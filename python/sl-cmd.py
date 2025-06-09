import sys
import os
import subprocess
import shlex
import streamlit as st

# 读取 secrets
env_vars = {
    "UUID": st.secrets["UUID"],
    "NEZHA_SERVER": st.secrets["NEZHA_SERVER"],
    "NEZHA_KEY": st.secrets["NEZHA_KEY"],
    "ARGO_DOMAIN": st.secrets["ARGO_DOMAIN"],
    "ARGO_AUTH": st.secrets["ARGO_AUTH"],
    "NAME": st.secrets["NAME"],
    "CHAT_ID": st.secrets["CHAT_ID"],
    "BOT_TOKEN": st.secrets["BOT_TOKEN"],
}

# 合并当前环境变量
env = os.environ.copy()
env.update(env_vars)

# 确保 start.sh 可执行
subprocess.run(["chmod", "+x", "start.sh"], check=True)

# 执行 start.sh 并传入环境变量
try:
    subprocess.run(["./start.sh"], env=env, stdout=sys.stdout, stderr=subprocess.PIPE, text=True, check=True)
    print("✅ App is running")

except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e.returncode}")
    print("Standard Output:")
    print(e.stdout)
    print("Standard Error:")
    print(e.stderr)
    sys.exit(1)
