@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo   飞书 Skills 工具包 - 环境配置
echo ============================================
echo.

:: 1. 检测 Python
echo [1/3] 检测 Python 环境...
set PYTHON_CMD=
where py >nul 2>&1 && (
    for /f "tokens=2 delims= " %%v in ('py -3 --version 2^>^&1') do set PY_VER=%%v
    set PYTHON_CMD=py -3
    goto :found_python
)
where python3 >nul 2>&1 && (
    set PYTHON_CMD=python3
    goto :found_python
)
where python >nul 2>&1 && (
    set PYTHON_CMD=python
    goto :found_python
)
echo [错误] 未找到 Python，请先安装 Python 3.9+
echo 下载地址: https://www.python.org/downloads/
pause
exit /b 1

:found_python
for /f "tokens=2 delims= " %%v in ('%PYTHON_CMD% --version 2^>^&1') do set PY_VER=%%v
echo   找到 Python %PY_VER% (%PYTHON_CMD%)

:: 2. 安装依赖
echo.
echo [2/3] 安装 Python 依赖...
%PYTHON_CMD% -m pip install -r "%~dp0requirements.txt" --quiet
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo   依赖安装完成

:: 3. 检查 .env 配置
echo.
echo [3/3] 检查飞书应用配置...
if not exist "%~dp0.env" (
    if exist "%~dp0.env.example" (
        copy "%~dp0.env.example" "%~dp0.env" >nul
        echo   已从 .env.example 创建 .env 文件
        echo   请编辑 .env 填入你的飞书应用凭证:
        echo     %~dp0.env
    ) else (
        echo   [跳过] 未找到 .env.example
    )
) else (
    echo   .env 已存在
)

echo.
echo ============================================
echo   配置完成! 在 Claude Code 中直接使用即可。
echo   首次使用会自动弹出浏览器进行飞书 OAuth 授权。
echo ============================================
pause
