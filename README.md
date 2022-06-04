# fastapi study

## Prerequirements
### Case 1. Github Codespace

Github 저장소에서 상단 [Code] 드롭다운 버튼을 눌러 'Create codespace on main' 을 선택한다.
필요한 환경이 구성되면서 vscode web이 싫행된다. 필요에 따라 에디터 좌하단 '>< Codespaces' 를 눌러 'Visual Studio Code 에서 열기'를 선택하거나 로컬 머신의 쉘에서 `gh codespace code` 를 입력하여 실행중인 원격 개발컨테이너를 네이티브 vscode 에서 연다.


### Case 2. Dev Containers

Github Codespace가 아직 활성화 되지 않았다면 로컬 머신에 실행중인 docker를 이용하여 동일한 환경의 개발 컨테이너를 로컬에 구성할 수 있다.
프로젝트를 열고 명령팔레트`⌘⇧P`에서 'Remote-Containers: Reopen in Container' 를 선택한다.

참조: https://code.visualstudio.com/docs/remote/containers-tutorial

### Case 3. Local

선호하는 virtualenvs 도구를 이용하여 python 3.10+ 을 구성하고 venv가 활성화된 상태에서 프로젝트를 연다.

## Installation

의존성 관리는 [flit](https://flit.pypa.io/en/latest/) 을 이용한다.
프로젝트 정보는 [PEP 517](https://peps.python.org/pep-0517/) 을 준수하는 `pyproject.toml` 을 이용한다.
필수가 아니라면 가급적 flit.* 확장 메타데이터는 쓰지 않는다.

```bash
$ pip install flit
$ flit install
```

## CLI

여러 회차에 걸친 fastapi app를 실행하기 위한 cli 커맨드

### Usage

```
Usage: main.py [OPTIONS]

  study apps cli
  ex) $ python main.py -a day1.homework -m app -p 4000 -r

Options:
  -a, --app TEXT      module name  [required]
  -m, --module TEXT   fast app instance
  -p, --port INTEGER  port number
  -r, --reload
  --help              Show this message and exit.
```

ex)

```bash
$ python main.py --app=day1.homework -r
```
