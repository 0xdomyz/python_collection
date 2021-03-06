from configparser import ConfigParser
from pathlib import Path


def read_config(path):
    cfg = ConfigParser()
    cfg.read(path)
    return cfg


def _get_list_from_config(section, option):
    return [i.lstrip() for i in cfg.get(section, option).split(",")]


if __name__ == "__main__":
    pth = Path(__file__).parent / "config"
    cfg = ConfigParser()
    cfg.read(pth)

    for i in cfg:
        print(i)
    cfg.get("section_9", "part1")
    cfg.has_option("section_10", "part1")
    cfg.has_option("section_10", "part4")
    cfg.has_section("section_10")
    cfg.has_section("section_11")
    cfg.add_section("section_11")
    cfg.set("section_11", "part2", "123")
    cfg["section_11"]["part66"]

    pth2 = pth.parent / "config2"
    with open(pth2, "w") as f:
        cfg.write(f)
    pth2.unlink()

    cfg = read_config(pth)
    {**cfg}
    [*cfg]
