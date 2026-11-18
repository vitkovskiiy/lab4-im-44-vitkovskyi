from tetris.cli import main


def test_main_prints_dropped_field_for_input_file_path(tmp_path, capsys):
    path = tmp_path / "input.txt"
    path.write_text("3 3\n.p.\n...\n#.#\n", encoding="utf-8")

    main([str(path)])

    assert capsys.readouterr().out == "...\n...\n#p#\n"


def test_main_prints_error_message_when_input_file_path_is_missing(capsys):
    main([])

    assert capsys.readouterr().out == "Error: invalid input\n"


def test_main_prints_error_message_for_file_that_is_not_utf8_text(tmp_path, capsys):
    # PowerShell 5.1 "echo ... > input.txt" writes UTF-16, which is not valid input.
    path = tmp_path / "input.txt"
    path.write_bytes("1 1\np\n".encode("utf-16"))

    main([str(path)])

    assert capsys.readouterr().out == "Error: invalid input\n"


def test_main_prints_error_message_when_input_file_does_not_exist(tmp_path, capsys):
    main([str(tmp_path / "missing.txt")])

    assert capsys.readouterr().out == "Error: invalid input\n"


def test_main_with_all_steps_flag_prints_every_step(tmp_path, capsys):
    path = tmp_path / "input.txt"
    path.write_text("3 1\np\n.\n#\n", encoding="utf-8")

    main(["--all-steps", str(path)])

    assert capsys.readouterr().out == "STEP 0\np\n.\n#\nSTEP 1\n.\np\n#\n"


def test_main_accepts_all_steps_flag_after_file_path(tmp_path, capsys):
    path = tmp_path / "input.txt"
    path.write_text("2 1\np\n.\n", encoding="utf-8")

    main([str(path), "--all-steps"])

    assert capsys.readouterr().out == "STEP 0\np\n.\nSTEP 1\n.\np\n"


def test_main_without_flag_still_prints_only_final_field(tmp_path, capsys):
    path = tmp_path / "input.txt"
    path.write_text("2 1\np\n.\n", encoding="utf-8")

    main([str(path)])

    assert capsys.readouterr().out == ".\np\n"


def test_main_prints_error_message_for_all_steps_flag_without_file_path(capsys):
    main(["--all-steps"])

    assert capsys.readouterr().out == "Error: invalid input\n"


def test_main_prints_error_message_for_two_file_paths(tmp_path, capsys):
    path = tmp_path / "input.txt"
    path.write_text("2 1\np\n.\n", encoding="utf-8")

    main([str(path), str(path)])

    assert capsys.readouterr().out == "Error: invalid input\n"
