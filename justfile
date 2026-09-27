default:
    @python main.py run

setup:
    @python main.py setup

test:
    @python main.py test

health:
    @python main.py health

clean:
    @python main.py clean

judge concept:
    @python main.py run --idea "{{concept}}"

audit path:
    @python main.py run --path "{{path}}"
