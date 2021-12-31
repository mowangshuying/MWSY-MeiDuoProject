#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MeiDuoMall.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # 上述导入可能由于其他原因而失败。确保
        # 问题是Django真的丢失了，以避免掩盖其他人
        # Python 2上的异常。
        try:
            import django
        except ImportError:
            raise ImportError(
                # 无法导入Django。您确定它已安装并且 在Python PATH环境变量上可用吗？
                # 忘记激活虚拟环境？
            )
        raise
    execute_from_command_line(sys.argv)
