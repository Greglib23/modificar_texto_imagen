import os
from gimpfu import *
import csv

def modificar_texto_imagen(csv_file,filename,output_dir,export_format): 
    # Read the data of csv
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    
    # Exit if the csv is empty
    if data == []:
        pdb.gimp_message("The csv is empty.")
        return
    
    # Creating the dir if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Obtener la imagen actual en el espacio de trabajo de GIMP
    image = gimp.image_list()
    if not image:
        pdb.gimp_message("There are no opened images at GIMP.")
        return   
    else:
        image = gimp.image_list()[0]
        
    # Read the layers of text
    textLayers = []
    for layer in image.layers:        
        if pdb.gimp_drawable_is_text_layer(layer):
            textLayers.append(layer)

    # Exit if no exists text layers
    if len(textLayers) == 0:
        pdb.gimp_message("There are no text layers.")
        return
    
    # Check if there are many text layers to the text of the csv
    if len(textLayers) != len(data[0]):
        pdb.gimp_message("Incompatible count of text layers with the count of columns in the csv. Text layers: {}. Csv Columns: {}".format(len(textLayers),len(data[0])))
        return

    count = 1
    for row in data:        
        for i , textLayer in enumerate(textLayers):
            pdb.gimp_text_layer_set_text(textLayer,row[i])
        new_image = pdb.gimp_image_duplicate(image)
        layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
        if export_format == "jpeg":
            pdb.file_jpeg_save(new_image, layer, output_dir + "\{}-{}.jpeg".format(filename,count) , filename + "-{}.jpeg".format(count),  0.9, 0, 0, 0, "", 0, 1, 0, 0)
        elif export_format == "png":
            pdb.file_png_save(new_image, layer, output_dir + "\{}-{}.png".format(filename,count) , filename + "-{}.png".format(count), 0, 9, 1, 1, 1, 1, 1)
        pdb.gimp_image_delete(new_image)

        count +=1

# Registro del plugin en GIMP
register(
    "python_fu_modificar_texto_imagen",
    "Modificar texto de imagen desde CSV",
    "Lee un archivo CSV y modifica el texto de una imagen en el espacio de trabajo, luego la exporta.",
    "Tu Nombre",
    "Tu Nombre",
    "2024",
    "Modificar Texto de Imagen...",
    "",  # Tipo de imagen que maneja el plugin
    [
        (PF_FILE, "csv_file", "Archivo CSV", ""),
        (PF_STRING, "filename", "Output: ",    "filename"),        
        (PF_DIRNAME, "output_dir", "Output dir:", os.path.expanduser("~")),
        (PF_RADIO, "export_format", "Export format: ", "jpeg", (("JPEG", "jpeg"), ("PNG", "png"))),
    ],
    [],
    modificar_texto_imagen,
    menu="<Image>/Filters/Modificar Texto CSV",
)

# Ejecutar el registro
main()
