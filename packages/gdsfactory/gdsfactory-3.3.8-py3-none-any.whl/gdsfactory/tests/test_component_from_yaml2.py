import pytest
from pytest_regressions.num_regression import NumericRegressionFixture

import gdsfactory as gf

mirror_port = """
instances:
    mmi_long:
      component: mmi1x2
      settings:
        width_mmi: 4.5
        length_mmi: 5
placements:
    mmi_long:
        port: o1
        x: 20
        y: 10
        mirror: True

ports:
    o1: mmi_long,o3
    o2: mmi_long,o2
    o3: mmi_long,o1
"""


mirror_x = """
instances:
    mmi_long:
      component: mmi1x2
      settings:
        width_mmi: 4.5
        length_mmi: 5
placements:
    mmi_long:
        x: 0
        y: 0
        mirror: 25
ports:
    o1: mmi_long,o3
    o2: mmi_long,o2
    o3: mmi_long,o1
"""


rotation = """
instances:
    mmi_long:
      component: mmi1x2
      settings:
        width_mmi: 4.5
        length_mmi: 5
placements:
    mmi_long:
        port: o1
        x: 10
        y: 20
        rotation: 90
ports:
    o1: mmi_long,o3
    o2: mmi_long,o2
    o3: mmi_long,o1
"""

dxdy = """
instances:
    mmi_long:
      component: mmi1x2
      settings:
        width_mmi: 4.5
        length_mmi: 10
    mmi_short:
      component: mmi1x2
      settings:
        width_mmi: 4.5
        length_mmi: 5

placements:
    mmi_short:
        port: o1
        x: 0
        y: 0
    mmi_long:
        port: o1
        x: mmi_short,o2
        y: mmi_short,o2
        dx: 10
        dy: -10
ports:
    o1: mmi_long,o3
"""


yaml_list = [mirror_port, mirror_x, rotation, dxdy]


@pytest.mark.parametrize("yaml_index", range(len(yaml_list)))
def test_components_ports(
    yaml_index: int, num_regression: NumericRegressionFixture
) -> None:
    yaml = yaml_list[yaml_index]
    c = gf.component_from_yaml(yaml)
    if c.ports:
        num_regression.check(c.get_ports_array())


if __name__ == "__main__":
    c = gf.component_from_yaml(mirror_port)
    c.show()
