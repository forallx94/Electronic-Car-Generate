import os, cv2, random ,argparse
from xml.etree.ElementTree import parse

class ElectronicCarGenerator:
  def __init__(self, save_path):
    self.save_path = save_path

    annotations_path = "./annotations"
    images_path = "./images"

    file_list = os.listdir(images_path)
    self.annotations = list()
    self.images = list()
    self.images_list = list()

    for file in file_list:
      tree = parse(os.path.join(annotations_path,file.rsplit('.')[0]+'.xml'))
      root = tree.getroot()
      plate_annotation = list()
      for object in root.iter("object"):
        plate_annotation.append([int(object.find("bndbox").findtext("xmin")),
                      int(object.find("bndbox").findtext("ymin")),
                      int(object.find("bndbox").findtext("xmax")),
                      int(object.find("bndbox").findtext("ymax"))])
      if len(plate_annotation) != 1:
        continue
      else:
        img = cv2.imread(os.path.join(images_path,file))
        self.images.append(img)
        self.annotations += plate_annotation
        self.images_list.append(file.rsplit('.')[0])

    self.image_len = len(self.images_list)
    # print('finish image load')

    # 모든 generate 이미지 로드
    # generate_path = "./generate"
    # file_list = os.listdir(generate_path)
    # self.generate = list()
    # self.generate_list = list()
    # for file in file_list:
    #   img = cv2.imread(os.path.join(generate_path,file))
    #   self.generate.append(img)
    #   self.generate_list.append(file.rsplit('.')[0])
    # self.generate_len = len(self.generate_list)
    

    # 특정 generate 이미지 로드
    self.generate_path = "./generate"
    self.generate_list = os.listdir(self.generate_path)
    self.generate_len = len(self.generate_list)
    # print('finish generate name load')

  def Generate_image(self, num, save = False):
    for i,iter in enumerate(range(num)):
      selected_image = random.randint(0,self.image_len-1)
      car = self.images[selected_image]
      label = self.annotations[selected_image]
      # print('finish select')
      
      selected_generate =  random.randint(0,self.generate_len)
      generate = cv2.imread(os.path.join(self.generate_path,self.generate_list[selected_generate]))
      # print('finish generate image load')

      name = self.images_list[selected_image] + '_' + self.generate_list[selected_generate]
      plate = cv2.resize(generate,(label[2]-label[0],label[3]-label[1]))
      car[label[1]:label[3],label[0]:label[2]] = plate
      # print('finish chage image')

      if save:
          cv2.imwrite(os.path.join(self.save_path , name) , car)
          # print('finish save image')
      else:
          cv2.imshow(label, car)
          cv2.waitKey(0)
          cv2.destroyAllWindows()


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--img_dir", help="save image directory",
                    type=str, default="../CRNN/DB/")
parser.add_argument("-n", "--num", help="number of image",
                    type=int)
parser.add_argument("-s", "--save", help="save or imshow",
                    type=bool, default=True)
args = parser.parse_args()


img_dir = args.img_dir
A = ElectronicCarGenerator(img_dir)

num_img = args.num
Save = args.save

A.Generate_image(num_img, save=Save)
print("Generate_image finish")