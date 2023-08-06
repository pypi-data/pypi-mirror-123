from service import service

@service
def fluxo(fn, args):
    fn.set_context(args)

    fn.add_step(executa1).when(lambda x: x == "2", "executa3")

    fn.add_step(executa2).when(lambda x: x == "0", "executa1")

    fn.add_step(executa3)

    return fn.step()


@service()
def executa(nome, sobrenome, fn):
    return nome[:2] + sobrenome[:2]


@service()
def concatenar_duas_letras_do_nome_e_sobrenome(nome, sobrenome, fn, **kwargs):

    if len(nome) < 2:
        fn.add_error("nome", "O nome está inválido", True)

    if len(sobrenome) < 2:
        fn.add_error("sobrenome", "O sobrenome está inválido")

    if len(nome) == 2:
        fn.add_message("deu certo mas... o nome parece errado.")

    if len(sobrenome) == 2:
        fn.add_message("deu certo mas... o sobrenome parece errado.")

    fn.validate()

    ret = executa(nome=nome, sobrenome=sobrenome)
    if ret.ok:
        return ret.value

    return "se ferrou se"


if __name__ == "__main__":
    result = concatenar_duas_letras_do_nome_e_sobrenome(nome="rafael", sobrenome="vettori")
    print(result)

    result = concatenar_duas_letras_do_nome_e_sobrenome(nome="", sobrenome="vettori")
    print(result)

    result = concatenar_duas_letras_do_nome_e_sobrenome(nome="ra", sobrenome="vettori")
    print(result)
