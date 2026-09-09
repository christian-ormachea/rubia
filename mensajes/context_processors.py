def chocolate_flag(request):
    mostrar = request.session.pop('mostrar_chocolate', False)
    return {'mostrar_chocolate_ahora': mostrar}