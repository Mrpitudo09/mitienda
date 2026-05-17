from flask import Flask, render_template, session, redirect, url_for, request, flash

app = Flask(__name__)
app.secret_key = "trendstore_secret_key_2024_xK9#mP"

# ==============================================================
# CATÁLOGO DE PRODUCTOS (Base de datos en memoria)
# ==============================================================
PRODUCTOS = [
    {
        "id": 1,
        "nombre": "Camiseta Essentials Blanca",
        "categoria": "Camisetas",
        "precio": 29.99,
        "descripcion": "Camiseta de algodón 100% orgánico con corte relajado. Perfecta para el día a día, combina con cualquier outfit. Disponible en talla S, M, L, XL.",
        "descripcion_corta": "Algodón orgánico, corte relajado. El básico perfecto.",
        "imagen": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80",
        "imagen_detalle": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=900&q=90",
        "stock": 15,
        "nuevo": True,
        "descuento": 0,
    },
    {
        "id": 2,
        "nombre": "Sudadera Oversize Gris",
        "categoria": "Sudaderas",
        "precio": 59.99,
        "descripcion": "Sudadera oversize con capucha en felpa de alta calidad. Interior suave y abrigado. Ideal para looks urbanos y casuales. Bolsillo canguro frontal.",
        "descripcion_corta": "Felpa premium, capucha y bolsillo canguro. Comodidad total.",
        "imagen": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=600&q=80",
        "imagen_detalle": "https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=900&q=90",
        "stock": 8,
        "nuevo": False,
        "descuento": 10,
    },
    {
        "id": 3,
        "nombre": "Chaqueta Vaquera Clásica",
        "categoria": "Chaquetas",
        "precio": 89.99,
        "descripcion": "Chaqueta vaquera de denim resistente con acabado vintage. Botones metálicos, dos bolsillos en el pecho y dos laterales. Una pieza atemporal para cualquier temporada.",
        "descripcion_corta": "Denim resistente con acabado vintage. Estilo atemporal.",
        "imagen": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=600&q=80",
        "imagen_detalle": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=900&q=90",
        "stock": 5,
        "nuevo": False,
        "descuento": 0,
    },
    {
        "id": 4,
        "nombre": "Pantalón Cargo Beige",
        "categoria": "Pantalones",
        "precio": 74.99,
        "descripcion": "Pantalón cargo con múltiples bolsillos utilitarios. Tejido de algodón resistente con ligero efecto desgastado. Cinturilla ajustable y corte recto moderno.",
        "descripcion_corta": "Múltiples bolsillos, algodón resistente. Estilo urbano.",
        "imagen": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&q=80",
        "imagen_detalle": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=900&q=90",
        "stock": 12,
        "nuevo": True,
        "descuento": 0,
    },
    {
        "id": 5,
        "nombre": "Bomber Jacket Negro",
        "categoria": "Chaquetas",
        "precio": 119.99,
        "descripcion": "Bomber jacket en nylon repelente al agua con relleno ligero. Cuello, puños y bajo en punto elástico. El outerwear más versátil de la temporada.",
        "descripcion_corta": "Nylon repelente, relleno ligero. El must-have de temporada.",
        "imagen": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600&q=80",
        "imagen_detalle": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=900&q=90",
        "stock": 7,
        "nuevo": True,
        "descuento": 15,
    },
    {
        "id": 6,
        "nombre": "Camiseta Gráfica Vintage",
        "categoria": "Camisetas",
        "precio": 34.99,
        "descripcion": "Camiseta con estampado gráfico de edición limitada. Algodón suave con lavado especial para efecto vintage. Cuello redondo reforzado. Serigrafía de alta durabilidad.",
        "descripcion_corta": "Edición limitada, efecto vintage. Diseño exclusivo.",
        "imagen": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=600&q=80",
        "imagen_detalle": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=900&q=90",
        "stock": 20,
        "nuevo": False,
        "descuento": 0,
    },
    {
        "id": 7,
        "nombre": "Hoodie Tie-Dye Multicolor",
        "categoria": "Sudaderas",
        "precio": 69.99,
        "descripcion": "Sudadera con capucha en técnica tie-dye artesanal. Cada pieza es única e irrepetible. Algodón grueso de 380g/m². Cordón ajustable y bolsillo central.",
        "descripcion_corta": "Tie-dye artesanal único, algodón 380g/m². Cada pieza es irrepetible.",
        "imagen": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=600&q=80",
        "imagen_detalle": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=900&q=90",
        "stock": 3,
        "nuevo": True,
        "descuento": 0,
    },
    {
        "id": 8,
        "nombre": "Trench Coat Camel",
        "categoria": "Abrigos",
        "precio": 159.99,
        "descripcion": "Trench coat clásico en color camel con doble botonadura. Cinturón ajustable en la cintura, hombreras discretas y forro interior satinado. La pieza más elegante de tu armario.",
        "descripcion_corta": "Doble botonadura, forro satinado. Elegancia atemporal.",
        "imagen": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=600&q=80",
        "imagen_detalle": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=900&q=90",
        "stock": 4,
        "nuevo": False,
        "descuento": 20,
    },
]


# ==============================================================
# FUNCIONES AUXILIARES
# ==============================================================
def obtener_producto_por_id(producto_id):
    """Busca y retorna un producto por su ID."""
    for producto in PRODUCTOS:
        if producto["id"] == producto_id:
            return producto
    return None


def calcular_precio_final(producto):
    """Calcula el precio con descuento aplicado."""
    if producto["descuento"] > 0:
        return round(producto["precio"] * (1 - producto["descuento"] / 100), 2)
    return producto["precio"]


def obtener_total_carrito():
    """Calcula el número total de ítems en el carrito."""
    carrito = session.get("carrito", {})
    return sum(item["cantidad"] for item in carrito.values())


# ==============================================================
# RUTAS
# ==============================================================

@app.route("/")
def index():
    """Página principal: muestra el catálogo completo."""
    categoria_filtro = request.args.get("categoria", "Todas")
    busqueda = request.args.get("q", "").strip().lower()

    productos_filtrados = PRODUCTOS

    if categoria_filtro != "Todas":
        productos_filtrados = [
            p for p in productos_filtrados if p["categoria"] == categoria_filtro
        ]

    if busqueda:
        productos_filtrados = [
            p for p in productos_filtrados
            if busqueda in p["nombre"].lower() or busqueda in p["categoria"].lower()
        ]

    categorias = sorted(list(set(p["categoria"] for p in PRODUCTOS)))

    productos_con_precio_final = []
    for p in productos_filtrados:
        p_copia = p.copy()
        p_copia["precio_final"] = calcular_precio_final(p)
        productos_con_precio_final.append(p_copia)

    return render_template(
        "index.html",
        productos=productos_con_precio_final,
        categorias=categorias,
        categoria_activa=categoria_filtro,
        busqueda=busqueda,
        total_carrito=obtener_total_carrito(),
    )


@app.route("/producto/<int:producto_id>")
def detalle_producto(producto_id):
    """Página de detalle de un producto específico."""
    producto = obtener_producto_por_id(producto_id)

    if not producto:
        flash("El producto que buscas no existe.", "error")
        return redirect(url_for("index"))

    producto_con_precio = producto.copy()
    producto_con_precio["precio_final"] = calcular_precio_final(producto)

    productos_relacionados = []
    for p in PRODUCTOS:
        if p["categoria"] == producto["categoria"] and p["id"] != producto_id:
            p_copia = p.copy()
            p_copia["precio_final"] = calcular_precio_final(p)
            productos_relacionados.append(p_copia)
            if len(productos_relacionados) == 3:
                break

    return render_template(
        "producto.html",
        producto=producto_con_precio,
        productos_relacionados=productos_relacionados,
        total_carrito=obtener_total_carrito(),
    )


@app.route("/carrito")
def ver_carrito():
    """Página del carrito de compras."""
    carrito_sesion = session.get("carrito", {})
    items_carrito = []
    subtotal = 0.0

    for producto_id_str, item in carrito_sesion.items():
        producto = obtener_producto_por_id(int(producto_id_str))
        if producto:
            precio_final = calcular_precio_final(producto)
            total_item = round(precio_final * item["cantidad"], 2)
            subtotal += total_item
            items_carrito.append(
                {
                    "id": producto["id"],
                    "nombre": producto["nombre"],
                    "imagen": producto["imagen"],
                    "categoria": producto["categoria"],
                    "precio_unitario": precio_final,
                    "cantidad": item["cantidad"],
                    "total_item": total_item,
                }
            )

    subtotal = round(subtotal, 2)
    envio = 4.99 if 0 < subtotal < 50 else 0.0
    total = round(subtotal + envio, 2)

    return render_template(
        "carrito.html",
        items=items_carrito,
        subtotal=subtotal,
        envio=envio,
        total=total,
        total_carrito=obtener_total_carrito(),
    )


@app.route("/carrito/agregar/<int:producto_id>", methods=["POST"])
def agregar_al_carrito(producto_id):
    """Agrega un producto al carrito en la sesión."""
    producto = obtener_producto_por_id(producto_id)

    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("index"))

    cantidad = int(request.form.get("cantidad", 1))
    if cantidad < 1:
        cantidad = 1
    if cantidad > producto["stock"]:
        cantidad = producto["stock"]

    if "carrito" not in session:
        session["carrito"] = {}

    carrito = session["carrito"]
    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        nueva_cantidad = carrito[producto_id_str]["cantidad"] + cantidad
        carrito[producto_id_str]["cantidad"] = min(nueva_cantidad, producto["stock"])
    else:
        carrito[producto_id_str] = {"cantidad": cantidad}

    session["carrito"] = carrito
    session.modified = True

    flash(f'"{producto["nombre"]}" añadido al carrito. 🛍️', "success")
    return redirect(request.referrer or url_for("index"))


@app.route("/carrito/eliminar/<int:producto_id>", methods=["POST"])
def eliminar_del_carrito(producto_id):
    """Elimina un producto completo del carrito."""
    if "carrito" in session:
        carrito = session["carrito"]
        producto_id_str = str(producto_id)
        if producto_id_str in carrito:
            del carrito[producto_id_str]
            session["carrito"] = carrito
            session.modified = True
            flash("Producto eliminado del carrito.", "info")

    return redirect(url_for("ver_carrito"))


@app.route("/carrito/actualizar/<int:producto_id>", methods=["POST"])
def actualizar_cantidad(producto_id):
    """Actualiza la cantidad de un producto en el carrito."""
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        return redirect(url_for("ver_carrito"))

    nueva_cantidad = int(request.form.get("cantidad", 1))

    if "carrito" in session:
        carrito = session["carrito"]
        producto_id_str = str(producto_id)
        if producto_id_str in carrito:
            if nueva_cantidad <= 0:
                del carrito[producto_id_str]
                flash("Producto eliminado del carrito.", "info")
            else:
                carrito[producto_id_str]["cantidad"] = min(
                    nueva_cantidad, producto["stock"]
                )
                flash("Cantidad actualizada.", "success")
            session["carrito"] = carrito
            session.modified = True

    return redirect(url_for("ver_carrito"))


@app.route("/carrito/vaciar", methods=["POST"])
def vaciar_carrito():
    """Vacía completamente el carrito."""
    session.pop("carrito", None)
    flash("Tu carrito ha sido vaciado.", "info")
    return redirect(url_for("ver_carrito"))


@app.route("/checkout")
def checkout():
    """Página de confirmación de pedido."""
    if not session.get("carrito"):
        flash("Tu carrito está vacío.", "info")
        return redirect(url_for("index"))
    session.pop("carrito", None)
    flash("✅ ¡Pedido realizado con éxito! Gracias por tu compra.", "success")
    return redirect(url_for("index"))


# ==============================================================
# MAIN
# ==============================================================
if __name__ == "__main__":
    app.run(debug=True)
