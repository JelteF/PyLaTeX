#!/usr/bin/python
"""
This example shows quantities functionality.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

# begin-doc-include
import quantities as pq

from pylatex import Document, Math, Quantity, Section, Subsection

if __name__ == "__main__":
    doc = Document()
    section = Section("Quantity tests")

    subsection = Subsection("Scalars with units")
    G = pq.constants.Newtonian_constant_of_gravitation
    moon_earth_distance = 384400 * pq.km
    moon_mass = 7.34767309e22 * pq.kg
    earth_mass = 5.972e24 * pq.kg
    moon_earth_force = G * moon_mass * earth_mass / moon_earth_distance**2
    q1 = Quantity(
        moon_earth_force.rescale(pq.newton),
        options={"round-precision": 4, "round-mode": "figures"},
    )
    math = Math(data=["F=", q1])
    subsection.append(math)
    section.append(subsection)

    subsection = Subsection("Scalars without units")
    world_population = 7400219037
    N = Quantity(
        world_population,
        options={"round-precision": 2, "round-mode": "figures"},
        format_cb="{0:23.17e}".format,
    )
    subsection.append(Math(data=["N=", N]))
    section.append(subsection)

    subsection = Subsection("Scalars with uncertainties")
    width = pq.UncertainQuantity(7.0, pq.meter, 0.4)
    length = pq.UncertainQuantity(6.0, pq.meter, 0.3)
    area = Quantity(
        width * length,
        options="separate-uncertainty",
        format_cb=lambda x: "{0:.1f}".format(float(x)),
    )
    subsection.append(Math(data=["A=", area]))
    section.append(subsection)

    doc.append(section)
    doc.generate_pdf("quantities_ex", clean_tex=False)
