import subprocess  # noqa: I005 S404


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_a28_package_no_param():
    command = ['a28', 'package']
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 package [-h] {init,build,install} ...'
    assert err[0:len(message)] == message


def test_a28_init_no_param():
    command = ['a28', 'package', 'init']
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 package init [-h] -s SCOPE -n NAME -t'
    assert err[0:len(message)] == message


def test_a28_build_no_param():
    command = ['a28', 'package', 'build']
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 package build [-h] --src SRC [--dest DEST]'
    assert err[0:len(message)] == message


def test_a28_install_no_param():
    command = ['a28', 'package', 'install']
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 package install [-h] --pkg PKG'
    assert err[0:len(message)] == message
