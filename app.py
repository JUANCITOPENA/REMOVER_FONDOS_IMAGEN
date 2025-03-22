import streamlit as st
from rembg import remove
from PIL import Image, ImageEnhance
import io

def enhance_image(image):
    """Mejora el contraste de la imagen para optimizar la eliminación del fondo."""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(1.5)  # Aumentar el contraste

def main():
    st.title("🖼️ REMOVER FONDO DE IMÁGENES ✂️")

    st.markdown(
        "<h4 style='text-align: center; color: gray;'>Creado por Juancito Peña</h4>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Elige un archivo de imagen (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGBA")
        enhanced_image = enhance_image(image)

        # Convertir imagen a bytes
        img_byte_arr = io.BytesIO()
        enhanced_image.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        # Remover fondo
        result_bytes = remove(img_bytes)
        img_no_bg = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

        st.image(img_no_bg, caption="Imagen sin fondo", use_container_width=True)

        # Descarga con recarga automática
        st.download_button(
            label="💾 Descargar imagen sin fondo",
            data=img_bytes,
            file_name="imagen_sin_fondo.png",
            mime="image/png"
        )

        # JavaScript para recargar la página después de la acción
        st.markdown(
            """
            <script>
            document.querySelector('button[download]').addEventListener('click', function() {
                setTimeout(function() {
                    location.reload();
                }, 1000); // Recarga en 1 segundo después del clic
            });
            </script>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
