import subprocess  # noqa: I005 S404


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_a28_no_param():
    command = ['a28']
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 [-h] [-v] {package,pkg,system,sys} ...'
    assert err[0:len(message)] == message


def test_a28_version_param():
    command = ['a28', '-v']
    out, err, exitcode = capture(command)
    assert exitcode == 0
    message = b'a28 version '
    assert out[0:len(message)] == message
    message = b''
    assert err[0:len(message)] == message
