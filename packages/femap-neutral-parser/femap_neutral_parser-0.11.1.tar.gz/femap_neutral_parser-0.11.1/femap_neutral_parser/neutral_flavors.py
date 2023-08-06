"""
Common mappings for MYSTRAN and FEMAP
for each self.flavor, describe vectors in terms of (<vector>, <axis>)
"""
from collections import defaultdict

from femap_neutral_parser.utils import CaseInsensitiveDict


HEADERS_TO_NEUTRAL = {
    ("applied_gpf", "r1"): ["R1 Applied GPMoment"],
    ("applied_gpf", "r2"): ["R2 Applied GPMoment"],
    ("applied_gpf", "r3"): ["R3 Applied GPMoment"],
    ("applied_gpf", "r_total"): ["Total Applied GPMoment"],
    ("applied_gpf", "t1"): ["T1 Applied GPForce"],
    ("applied_gpf", "t2"): ["T2 Applied GPForce"],
    ("applied_gpf", "t3"): ["T3 Applied GPForce"],
    ("applied_gpf", "t_total"): ["Total Applied GPForce"],
    ("cbar_ms", "compression"): ["Bar Compression M.S."],
    ("cbar_ms", "tension"): ["Bar Tension M.S."],
    ("cbush_stress", "r1"): ["Bush r1 Stress"],  # as pynastran
    ("cbush_stress", "r2"): ["Bush r2 Stress"],  # as pynastran
    ("cbush_stress", "r3"): ["Bush r3 Stress"],  # as pynastran
    ("cbush_stress", "t1"): ["Bush t1 Stress"],  # as pynastran
    ("cbush_stress", "t2"): ["Bush t2 Stress"],  # as pynastran
    ("cbush_stress", "t3"): ["Bush t3 Stress"],  # as pynastran
    ("constraint_gpf", "r1"): ["R1 Constraint GPMoment"],
    ("constraint_gpf", "r2"): ["R2 Constraint GPMoment"],
    ("constraint_gpf", "r3"): ["R3 Constraint GPMoment"],
    ("constraint_gpf", "r_total"): ["Total Constraint GPMoment"],
    ("constraint_gpf", "t1"): ["T1 Constraint GPForce"],
    ("constraint_gpf", "t2"): ["T2 Constraint GPForce"],
    ("constraint_gpf", "t3"): ["T3 Constraint GPForce"],
    ("constraint_gpf", "t_total"): ["Total Constraint GPForce"],
    ("displacements", "r1"): ["R1 rotation", "R1 Rotation"],  # as pynastran
    ("displacements", "r2"): ["R2 rotation", "R2 Rotation"],  # as pynastran
    ("displacements", "r3"): ["R3 rotation", "R3 Rotation"],  # as pynastran
    ("displacements", "r_total"): ["RSS rotation", "Total Rotation"],  # as pynastran
    ("displacements", "t1"): ["T1 translation", "T1 Translation"],  # as pynastran
    ("displacements", "t2"): ["T2 translation", "T2 Translation"],  # as pynastran
    ("displacements", "t3"): ["T3 translation", "T3 Translation"],  # as pynastran
    ("displacements", "t_total"): [
        "RSS translation",
        "Total Translation",
    ],  # as pynastran
    ("elem_gpf", "c1_r1"): ["Elem C1 R1 GPMoment"],
    ("elem_gpf", "c1_r2"): ["Elem C1 R2 GPMoment"],
    ("elem_gpf", "c1_r3"): ["Elem C1 R3 GPMoment"],
    ("elem_gpf", "c1_t1"): ["Elem C1 T1 GPForce"],
    ("elem_gpf", "c1_t2"): ["Elem C1 T2 GPForce"],
    ("elem_gpf", "c1_t3"): ["Elem C1 T3 GPForce"],
    ("elem_gpf", "c2_r1"): ["Elem C2 R1 GPMoment"],
    ("elem_gpf", "c2_r2"): ["Elem C2 R2 GPMoment"],
    ("elem_gpf", "c2_r3"): ["Elem C2 R3 GPMoment"],
    ("elem_gpf", "c2_t1"): ["Elem C2 T1 GPForce"],
    ("elem_gpf", "c2_t2"): ["Elem C2 T2 GPForce"],
    ("elem_gpf", "c2_t3"): ["Elem C2 T3 GPForce"],
    ("force_vectors", "r1"): ["R1 applied moment", "R1 Applied Moment"],  # as pynastran
    ("force_vectors", "r2"): ["R2 applied moment", "R2 Applied Moment"],  # as pynastran
    ("force_vectors", "r3"): ["R3 applied moment", "R3 Applied Moment"],  # as pynastran
    ("force_vectors", "r_total"): [
        "RSS applied moment",
        "Total Applied Moment",
    ],  # as pynastran
    ("force_vectors", "t1"): ["T1 applied force", "T1 Applied Force"],  # as pynastran
    ("force_vectors", "t2"): ["T2 applied force", "T2 Applied Force"],  # as pynastran
    ("force_vectors", "t3"): ["T3 applied force", "T3 Applied Force"],  # as pynastran
    ("force_vectors", "t_total"): [
        "RSS applied force",
        "Total Applied Force",
    ],  # as pynastran
    ("cbar_force", "axial_a"): [
        "BAR EndA Axial Force",
        "Bar EndA Axial Force",
    ],  # as pynastran
    ("cbar_force", "axial_b"): ["BAR EndB Axial Force"],  # as pynastran
    ("cbar_force", "bending_moment_a1"): [  # as pynastran
        "BAR EndA Plane1 Moment",
        "Bar EndA Plane1 Moment",
    ],
    ("cbar_force", "bending_moment_a2"): [  # as pynastran
        "BAR EndA Plane2 Moment",
        "Bar EndA Plane2 Moment",
    ],
    ("cbar_force", "bending_moment_b1"): [  # as pynastran
        "BAR EndB Plane1 Moment",
        "Bar EndB Plane1 Moment",
    ],
    ("cbar_force", "bending_moment_b2"): [  # as pynastran
        "BAR EndB Plane2 Moment",
        "Bar EndB Plane2 Moment",
    ],
    ("cbar_force", "shear_a1"): [  # as pynastran
        "BAR EndA Pl1 Shear Force",
        "Bar EndA Pl1 Shear Force",
    ],
    ("cbar_force", "shear_a2"): [  # as pynastran
        "BAR EndA Pl2 Shear Force",
        "Bar EndA Pl2 Shear Force",
    ],
    ("cbar_force", "shear_b1"): ["BAR EndB Pl1 Shear Force"],  # as pynastran
    ("cbar_force", "shear_b2"): ["BAR EndB Pl2 Shear Force"],  # as pynastran
    ("cbar_force", "torque_a"): ["BAR EndA Torque", "Bar EndA Torque"],  # as pynastran
    ("cbar_force", "torque_b"): ["BAR EndB Torque"],  # as pynastran
    ("cbush_force", "r1"): ["BUSH Moment XE", "Bush X Moment"],  # as pynastran
    ("cbush_force", "r2"): ["BUSH Moment YE", "Bush Y Moment"],  # as pynastran
    ("cbush_force", "r3"): ["BUSH Moment ZE", "Bush Z Moment"],  # as pynastran
    ("cbush_force", "t1"): ["BUSH Force XE", "Bush X Force"],  # as pynastran
    ("cbush_force", "t2"): ["BUSH Force YE", "Bush Y Force"],  # as pynastran
    ("cbush_force", "t3"): ["BUSH Force ZE", "Bush Z Force"],  # as pynastran
    ("spc_forces", "r1"): ["R1 SPC moment", "R1 Constraint Moment"],  # as pynastran
    ("spc_forces", "r2"): ["R2 SPC moment", "R2 Constraint Moment"],  # as pynastran
    ("spc_forces", "r3"): ["R3 SPC moment", "R3 Constraint Moment"],  # as pynastran
    ("spc_forces", "r_total"): [
        "RSS SPC moment",
        "Total Constraint Moment",
    ],  # as pynastran
    ("spc_forces", "t1"): ["T1 SPC force", "T1 Constraint Force"],  # as pynastran
    ("spc_forces", "t2"): ["T2 SPC force", "T2 Constraint Force"],  # as pynastran
    ("spc_forces", "t3"): ["T3 SPC force", "T3 Constraint Force"],  # as pynastran
    ("spc_forces", "t_total"): [
        "RSS SPC force",
        "Total Constraint Force",
    ],  # as pynastran
    ("mpc_forces", "r1"): ["R1 MultiPoint Moment"],  # as pynastran
    ("mpc_forces", "r2"): ["R2 MultiPoint Moment"],  # as pynastran
    ("mpc_forces", "r3"): ["R3 MultiPoint Moment"],  # as pynastran
    ("mpc_forces", "r_total"): ["Total MultiPoint Moment"],  # as pynastran
    ("mpc_forces", "t1"): ["T1 MultiPoint Force"],  # as pynastran
    ("mpc_forces", "t2"): ["T2 MultiPoint Force"],  # as pynastran
    ("mpc_forces", "t3"): ["T3 MultiPoint Force"],  # as pynastran
    ("mpc_forces", "t_total"): ["Total MultiPoint Force"],  # as pynastran
    ("cbar_stress", "axial_a"): ["Bar EndA Axial Stress"],  # as pynastran
    ("cbar_stress", "bend_a1"): ["Bar EndA Pt1 Bend Stress"],  # as pynastran
    ("cbar_stress", "bend_a2"): ["Bar EndA Pt2 Bend Stress"],  # as pynastran
    ("cbar_stress", "bend_a3"): ["Bar EndA Pt3 Bend Stress"],  # as pynastran
    ("cbar_stress", "bend_a4"): ["Bar EndA Pt4 Bend Stress"],  # as pynastran
    ("cbar_stress", "bend_b1"): ["Bar EndB Pt1 Bend Stress"],  # as pynastran
    ("cbar_stress", "bend_b2"): ["Bar EndB Pt2 Bend Stress"],  # as pynastran
    ("cbar_stress", "bend_b3"): ["Bar EndB Pt3 Bend Stress"],  # as pynastran
    ("cbar_stress", "bend_b4"): ["Bar EndB Pt4 Bend Stress"],  # as pynastran
    ("cbar_stress", "comb_a1"): ["BAR EndA Pt1 Comb Stress"],  # as pynastran
    ("cbar_stress", "comb_a2"): ["BAR EndA Pt2 Comb Stress"],  # as pynastran
    ("cbar_stress", "comb_a3"): ["BAR EndA Pt3 Comb Stress"],  # as pynastran
    ("cbar_stress", "comb_a4"): ["BAR EndA Pt4 Comb Stress"],  # as pynastran
    ("cbar_stress", "comb_b1"): ["BAR EndB Pt1 Comb Stress"],  # as pynastran
    ("cbar_stress", "comb_b2"): ["BAR EndB Pt2 Comb Stress"],  # as pynastran
    ("cbar_stress", "comb_b3"): ["BAR EndB Pt3 Comb Stress"],  # as pynastran
    ("cbar_stress", "comb_b4"): ["BAR EndB Pt4 Comb Stress"],  # as pynastran
    ("cbar_stress", "max_comb_a"): [
        "BAR EndA Max Stress",
        "Bar EndA Max Comb Stress",
    ],  # as pynastran
    ("cbar_stress", "max_comb_b"): [
        "BAR EndB Max Stress",
        "Bar EndB Max Comb Stress",
    ],  # as pynastran
    ("cbar_stress", "min_comb_a"): [
        "BAR EndA Min Stress",
        "Bar EndA Min Comb Stress",
    ],  # as pynastran
    ("cbar_stress", "min_comb_b"): [
        "BAR EndB Min Stress",
        "Bar EndB Min Comb Stress",
    ],  # as pynastran
    ("summed_gpf", "r1"): ["R1 Summed GPMoment"],
    ("summed_gpf", "r2"): ["R2 Summed GPMoment"],
    ("summed_gpf", "r3"): ["R3 Summed GPMoment"],
    ("summed_gpf", "r_total"): ["Total Summed GPMoment"],
    ("summed_gpf", "t1"): ["T1 Summed GPForce"],
    ("summed_gpf", "t2"): ["T2 Summed GPForce"],
    ("summed_gpf", "t3"): ["T3 Summed GPForce"],
    ("summed_gpf", "t_total"): ["Total Summed GPForce"],
}
# ALIASES are used to restrict `get_vectors` returned values
ALIASES = {
    "cbar_force": {
        "axial_b": "axial",
        "axial_a": "axial",
        "torque_b": "torque",
        "torque_a": "torque",
        "shear_a2": "shear2",
        "shear_a1": "shear1",
        "shear_b2": "shear2",
        "shear_b1": "shear1",
    }
}

REVERTED_ALIASES = {}
for vector, merges in ALIASES.items():
    REVERTED_ALIASES[vector] = {v: k for k, v in merges.items()}

# =============================================================================
# the following boilerplate is purely cosmetcis and ensure that
# engineering high-level functions will get t1 before r1
# =============================================================================
HEADERS_TO_NEUTRAL = list(HEADERS_TO_NEUTRAL.items())
# tercery key
HEADERS_TO_NEUTRAL = sorted(HEADERS_TO_NEUTRAL, key=lambda x: x[0][1], reverse=False)
# secondary key: sort by <axis> first letter, "t" before "r"
HEADERS_TO_NEUTRAL = sorted(HEADERS_TO_NEUTRAL, key=lambda x: x[0][1][0], reverse=True)
# primary key: sort by <vector>
HEADERS_TO_NEUTRAL = sorted(HEADERS_TO_NEUTRAL, key=lambda x: x[0][0], reverse=False)
# and go back to dict...
HEADERS_TO_NEUTRAL = dict(HEADERS_TO_NEUTRAL)
# -----------------------------------------------------------------------------
# prepare reversed search
# "RSS translation" -> ("displacements", "t_total")  # as pynastran
NEUTRAL_TO_HEADERS = CaseInsensitiveDict()
for headers, titles in HEADERS_TO_NEUTRAL.items():
    for title in titles:
        if title:
            if title in NEUTRAL_TO_HEADERS and headers != NEUTRAL_TO_HEADERS[title]:
                raise ValueError(
                    f"CaseInsensitiveDict cannot handle a different {title=}\nAlready stored {NEUTRAL_TO_HEADERS[title]}\nWant to add {headers}"
                )
            NEUTRAL_TO_HEADERS[title] = headers


class Flavor:
    """Mixin handling neutral self.flavor

    >>> f = Flavor()
    >>> f.title_to_headers("T1 translation")
    ('displacements', 't1')
    >>> f.title_to_headers("t1 TrAnslation")
    ('displacements', 't1')
    """

    def title_to_headers(self, key, merge_aliases=False):
        """Convert Neutral title to headers tuple:

        >>> f = Flavor()
        >>> f.title_to_headers("T1 translation")
        ('displacements', 't1')
        >>> f.title_to_headers("BAR EndA Torque")
        ('cbar_force', 'torque_a')
        >>> f.title_to_headers("BAR EndA Torque", merge_aliases=True)
        ('cbar_force', 'torque')
        """
        headers = NEUTRAL_TO_HEADERS.get(key)
        if not headers:
            # return initial FEMAP/MYSTRAN title
            return key
        vector, axis = headers
        if merge_aliases:
            # check if an alias esits
            aliases = ALIASES.get(vector)
            if aliases:
                axis = aliases.get(axis, axis)
        return (vector, axis)

    def headers_to_title(self, key):
        """search for `key` in `self.flavor` dict
        >>> f = Flavor()
        >>> f.headers_to_title(("displacements", "t1"))
        'T1 translation'
        >>> f.headers_to_title("displacements::t1")
        'T1 translation'
        >>> f.headers_to_title(('cbar_force', 'torque_a'))
        'BAR EndA Torque'
        >>> f.headers_to_title(('cbar_force', 'torque_a'))
        'BAR EndA Torque'
        >>> f.headers_to_title(('cbar_force', 'torque'))
        'BAR EndA Torque'
        """
        if isinstance(key, str):
            vector, axis = key.split("::")
        else:
            # assumed a correct tuple was passed
            vector, axis = key
        try:
            axis = REVERTED_ALIASES[vector][axis]
        except KeyError:
            pass  # no alias
        title = HEADERS_TO_NEUTRAL[(vector, axis)][0]
        return title

    @classmethod
    def get_vectors(self, what=None, merge_aliases=False):
        """
        return a list of relevant vectors
        >>> f = Flavor()
        >>> f.get_vectors("cbar_force") == [
        ... 'cbar_force::torque_a',
        ... 'cbar_force::torque_b',
        ... 'cbar_force::shear_a1',
        ... 'cbar_force::shear_a2',
        ... 'cbar_force::shear_b1',
        ... 'cbar_force::shear_b2',
        ... 'cbar_force::bending_moment_a1',
        ... 'cbar_force::bending_moment_a2',
        ... 'cbar_force::bending_moment_b1',
        ... 'cbar_force::bending_moment_b2',
        ... 'cbar_force::axial_a',
        ... 'cbar_force::axial_b']
        True

        If merge_aliases is `True`::
        >>> f.get_vectors("cbar_force", merge_aliases=True) == [
        ... 'cbar_force::bending_moment_a1',
        ... 'cbar_force::bending_moment_a2',
        ... 'cbar_force::bending_moment_b1',
        ... 'cbar_force::bending_moment_b2',
        ... 'cbar_force::axial',
        ... 'cbar_force::shear1',
        ... 'cbar_force::shear2',
        ... 'cbar_force::torque']
        True

        Ommitting key will give access to available vectors families::
        >>> sorted(list(f.get_vectors()))
        ['applied_gpf', 'cbar_force', ..., 'spc_forces', 'summed_gpf']

        """
        dic = defaultdict(list)
        for (vector, axis), initial_title in HEADERS_TO_NEUTRAL.items():
            dic[vector].append(axis)
        dic = dict(dic)
        # -> {..., 'cbar_force': ['torque_a', 'torque_b',...], ...}
        if merge_aliases:
            for vector, merges in ALIASES.items():
                dic[vector] = [axis for axis in dic[vector] if axis not in merges]
                dic[vector] += sorted(list(set(merges.values())))
        if what is not None:
            return [f"{what}::{t}" for t in dic[what]]
        return set(dic.keys())


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
