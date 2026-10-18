import os, resource, subprocess, sys, time
# usage: measure_dcpo.py <threads> <film_dir>
threads, film = sys.argv[1], sys.argv[2]
env = dict(os.environ)
b = env["DCPO_BIN"]
t0 = time.time()
p = subprocess.Popen([b + "/dcpomatic2_cli", "-n", "-r", "-t", threads, "-d", "make-dcp", film], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
peak_kb = 0
while p.poll() is None:
    try:
        with open(f"/proc/{p.pid}/status") as f:
            for line in f:
                if line.startswith("VmHWM:"):
                    peak_kb = max(peak_kb, int(line.split()[1]))
    except Exception:
        pass
    time.sleep(0.05)
out, err = p.communicate()
wall = time.time() - t0
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
print(f"threads={threads} exit={p.returncode} wall_s={wall:.2f} user_s={ru.ru_utime:.2f} sys_s={ru.ru_stime:.2f} maxrss_MB={ru.ru_maxrss/1024:.0f} sampled_VmHWM_MB={peak_kb/1024:.0f}")
print("stdout:", out.decode()[-400:].strip())
print("stderr:", err.decode()[-600:].strip())
