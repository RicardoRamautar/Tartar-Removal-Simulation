from modules.config import *

class gradientField():
    def __init__(self, properties, x_image, y_image, A=500, screen_dimensions=[screen_width,screen_height]):
        self.A = A 
        self.x_image = x_image
        self.y_image = y_image

        self.topleft = self.position_ellipses(properties)

        self.xc = self.topleft[0] + properties[2]/2
        self.yc = self.topleft[1] + properties[3]/2

        self.width  = int(np.round(properties[2], 0))
        self.height = int(np.round(properties[3], 0))

        self.grid_size = screen_dimensions

        self.height_map = self.generate_height_map()

        self.dy, self.dx = self.generate_gradient()

    def __str__(self):
        return f'Gradient Field at ({self.xc},{self.yc}) with width {self.width} and height {self.height}'
    
    def position_ellipses(self, properties):
        topleft = np.array([properties[0] - jaw_image.get_width()/2,
                            properties[1] - jaw_image.get_height()/2])
        
        R = np.array([[-1, 0],
                      [0,-1]])

        topleft = R.dot(topleft) + np.array([jaw_image.get_width()/2, 
                                                  jaw_image.get_height()/2])
        
        topleft -= np.array([properties[2], properties[3]])

        topleft += np.array([self.x_image, self.y_image])

        return topleft

    def generate_height_map(self):
        x, y = np.meshgrid(np.linspace(0, self.grid_size[0]-1, self.grid_size[0]), 
                        np.linspace(0, self.grid_size[1]-1, self.grid_size[1]), indexing='xy')

        sigma_x = self.width / np.sqrt(2)
        sigma_y = self.height / np.sqrt(2)

        g = self.A * np.exp(-((x - self.xc) ** 2 / (2 * sigma_x ** 2) + (y - self.yc) ** 2 / (2 * sigma_y ** 2)))
        print(f'Generated height map with shape {g.shape}')
        return g

    def generate_gradient(self):
        return np.gradient(self.height_map)