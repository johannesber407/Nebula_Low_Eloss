#ifndef __PARTICLE_OUTPUT_H_
#define __PARTICLE_OUTPUT_H_

#include <array>
#include "output_stream.h"
#include "load_pri_file.h"

template<
	bool save_pld = true,
	bool save_scattering = true,
	bool save_primary_secondary = true>
struct particle_output
{

    /**
	 * \brief Print diagnostic info
	 */
	static void print_info(std::ostream& stream)
	{
		stream << std::boolalpha <<
			" * Data output format\n"
			"   Options:\n"
			"     - Path length: " << save_pld << "\n"
			"     - Scattering: " << save_scattering << "\n"
			"     - Primary/Secondary: " << save_primary_secondary << "\n";
	}

	static constexpr size_t float_count = 7
		+ (save_pld ? 1 : 0)
		+ (save_scattering ? 6 : 0);
	static constexpr size_t int_count = 2 + (save_primary_secondary ? 1 : 0);
	static constexpr size_t row_size = float_count*sizeof(float) + int_count*sizeof(int);

	static void add(
		output_buffer& buffer,
		particle const & p,
		int2 pixel,
		real path_length,
		uint32_t n_elastic,
		uint32_t n_inelastic,
		uint32_t n_surface,
		real elastic_loss,
		real inelastic_loss,
		real surface_loss,
		bool secondary)
	{
		std::array<float, float_count> floats{};
		size_t i = 0;
		floats[i++] = p.pos.x;
		floats[i++] = p.pos.y;
		floats[i++] = p.pos.z;
		floats[i++] = p.dir.x;
		floats[i++] = p.dir.y;
		floats[i++] = p.dir.z;
		floats[i++] = p.kin_energy;
		if (save_pld)
			floats[i++] = static_cast<float>(path_length);
		if (save_scattering)
			floats[i++] = static_cast<float>(n_elastic);
		if (save_scattering)
			floats[i++] = static_cast<float>(n_inelastic);
		if (save_scattering)
			floats[i++] = static_cast<float>(n_surface);
		if (save_scattering)
			floats[i++] = static_cast<float>(elastic_loss);
		if (save_scattering)
			floats[i++] = static_cast<float>(inelastic_loss);
		if (save_scattering)
			floats[i++] = static_cast<float>(surface_loss);
		buffer.add(floats);

		std::array<int, int_count> ints{};
		ints[0] = pixel.x;
		ints[1] = pixel.y;
		if (save_primary_secondary)
			ints[2] = secondary ? 1 : 0;
		buffer.add(ints);
	}
};

#endif // __PARTICLE_OUTPUT_H_