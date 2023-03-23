from filesystem_autocomplete import walk_directory

dir_structure = {
    "dir1": ["iamafile.txt", "file2.what", "102.hmm"],
    "dir2": [
        {"dir3": ["another_level", "file3", "problem-file"]},
    ],
}


def test_walk_directory(tmp_path):
    d = tmp_path / "top_level"
    d.mkdir()

    p = d / "hello.txt"
    p.write_text("yup")

    d2 = d / "level_1_dir1"
    d2.mkdir()

    d3 = d / "level_1_dir2"
    d3.mkdir()

    d4 = d3 / "level_2_dir1"
    d4.mkdir()

    d2fi = d2 / "problem-file.whatever.txt"
    d2fi.write_text("test")

    for fi in "123":
        d3fi = d3 / f"test_file_{fi}.txt"
        d3fi.write_text("test")

        d4fi = d4 / f"test_file_{fi}.txt"
        d4fi.write_text("a different test")

    dir_info = walk_directory(str(d))

    assert hasattr(dir_info, "level_1_dir1")
    assert hasattr(dir_info, "level_1_dir2")

    for fi in "123":
        fname_orig = f"test_file_{fi}.txt"
        fname = fname_orig.replace(".", "_")
        assert hasattr(dir_info.level_1_dir2, fname)
        assert hasattr(dir_info.level_1_dir2.level_2_dir1, fname)

        thepath = getattr(dir_info.level_1_dir2, fname).filepath
        assert thepath == str(d3 / fname_orig)

    thepath = dir_info.level_1_dir2.dirpath
    assert thepath == str(d3)
