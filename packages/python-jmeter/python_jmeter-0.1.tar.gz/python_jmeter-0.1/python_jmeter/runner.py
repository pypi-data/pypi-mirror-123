import os
import subprocess

from python_jmeter import builder


def run(request, obj, debug=False, gui=False):
    test_plan_dir = builder.build_jmx(obj)
    jmx_file = os.path.join(test_plan_dir, f'testplan_{obj.id}.jmx')
    report_html_dir = os.path.join(test_plan_dir, 'report_html')
    report_file = os.path.join(test_plan_dir, 'report_jtl', 'report.jtl')
    log_file = os.path.join(test_plan_dir, f'run.log')

    run_cmd = f'jmeter -n -t {jmx_file} -l {report_file} -j {log_file}'
    report_cmd = f'jmeter -g {report_file} -o {report_html_dir}'

    if gui is True:
        return os.system(f'jmeter -t {jmx_file}')

    if debug is True:
        return os.system(run_cmd)

    p1 = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE)
    # output1 = p1.stdout.read().decode('utf-8')
    if request.is_websocket():
        while True:
            data = p1.stdout.readline().decode('utf-8').strip()
            if data == b'' and p1.poll() is not None:
                break
            print(data)
            request.websocket.send(data)
    return ''


    p2 = subprocess.Popen(report_cmd, shell=True, stdout=subprocess.PIPE)
    # print(p2.stdout.read().decode('utf-8'))
    # return output1


if __name__ == '__main__':
    t = models.TestPlan.objects.get(id=1)
    # run(t, debug=True)
    run(t)
