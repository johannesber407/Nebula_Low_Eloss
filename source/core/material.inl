#include <initializer_list>

namespace detail
{
	template<typename source_type, typename... target_scatter_types, size_t... is>
	scatter_list<target_scatter_types...> create_scatter_list(
		source_type const & source,
		nbl::index_sequence<is...>)
	{
		return { target_scatter_types::create(
			nbl::tuple::get<is>(source))... };
	}

	template<typename... scatter_types, size_t... is>
	void destroy_scatter_list(
		scatter_list<scatter_types...> & list,
		nbl::index_sequence<is...>)
	{
		(void)std::initializer_list<int>{
			(scatter_types::destroy(nbl::tuple::get<is>(list)), 0)... };
	}
}

template<typename... scatter_types>
CPU auto material<scatter_list<scatter_types...>>::create(nbl::hdf5_file const & mat)
	-> material
{
	material<base_t> target;

	target.barrier = static_cast<real>(mat.get_property_quantity("barrier") / nbl::units::eV);
	if (mat.exists("/surface_excitation"))
	{
		if (!mat.exists("/surface_excitation/parameter") ||
			!mat.exists("/surface_excitation/elf"))
			throw std::runtime_error("Incomplete surface excitation data in material file " + mat.get_filename());

		auto parameter = mat.fill_table1D<real>("/surface_excitation/parameter");
		if (parameter.width() != 1)
			throw std::runtime_error("Surface excitation parameter must contain one value in material file " + mat.get_filename());
		target.surface_excitation_parameter = parameter(0);
		nbl::util::table_1D<real, false>::destroy(parameter);

		auto surface_elf = mat.fill_table1D<real>("/surface_excitation/elf");
		const auto surface_energy = mat.get_dimscale("/surface_excitation/elf", 0,
			surface_elf.width());
		if (surface_elf.width() < 2)
			throw std::runtime_error("Surface ELF must contain at least two values in material file " + mat.get_filename());
		surface_elf.set_scale(
			static_cast<real>(surface_energy.front() / nbl::units::eV),
			static_cast<real>(surface_energy.back() / nbl::units::eV));

		std::vector<real> cumulative(surface_elf.width(), 0);
		for (int i = 1; i < surface_elf.width(); ++i)
		{
			const real dx = static_cast<real>((surface_energy[i] - surface_energy[i - 1]) / nbl::units::eV);
			cumulative[i] = cumulative[i - 1] + dx *
				(0.5_r * maxr(0, surface_elf(i - 1)) + 0.5_r * maxr(0, surface_elf(i)));
		}

		const real integral = cumulative.back();
		if (integral <= 0)
			throw std::runtime_error("Surface ELF must have a positive integral in material file " + mat.get_filename());

		std::vector<real> surface_icdf(surface_elf.width());
		for (int i = 0; i < surface_elf.width(); ++i)
		{
			const real target = integral * i / (surface_elf.width() - 1);
			int j = 1;
			while (j < surface_elf.width() - 1 && cumulative[j] <= target)
				++j;
			const real fraction = cumulative[j] == cumulative[j - 1] ? 0 :
				(target - cumulative[j - 1]) / (cumulative[j] - cumulative[j - 1]);
			surface_icdf[i] = static_cast<real>(surface_energy[j - 1] / nbl::units::eV) +
				static_cast<real>((surface_energy[j] - surface_energy[j - 1]) / nbl::units::eV) * fraction;
		}
		auto surface_icdf_table = nbl::util::table_1D<real, false>::create(
			0, 1, surface_elf.width(), surface_icdf.data());
		target.surface_elf = nbl::util::table_1D<real,
			detail::material_storage_traits<scatter_types...>::is_gpu>::create(surface_icdf_table);
		nbl::util::table_1D<real, false>::destroy(surface_icdf_table);
	}
	target.base_t::operator=(base_t(scatter_types::create(mat)...));

	return target;
}

template<typename... scatter_types>
template<typename... source_scatter_types>
CPU auto material<scatter_list<scatter_types...>>::create(
	material<scatter_list<source_scatter_types...>> const & source)
	-> material
{
	material<base_t> target;

	target.barrier = source.barrier;
	target.surface_excitation_parameter = source.surface_excitation_parameter;
	target.surface_elf = nbl::util::table_1D<real,
		detail::material_storage_traits<scatter_types...>::is_gpu>::create(source.surface_elf);
	target.base_t::operator=(detail::create_scatter_list<
		scatter_list<source_scatter_types...>,
		scatter_types...>(source, nbl::make_index_sequence<sizeof...(scatter_types)>{}));

	return target;
}

template<typename... scatter_types>
CPU void material<scatter_list<scatter_types...>>::destroy(material & mat)
{
	nbl::util::table_1D<real,
		detail::material_storage_traits<scatter_types...>::is_gpu>::destroy(mat.surface_elf);
	detail::destroy_scatter_list(mat,
		nbl::make_index_sequence<sizeof...(scatter_types)>{});
}
