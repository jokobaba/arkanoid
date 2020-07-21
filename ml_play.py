"""
The template of the main script of the machine learning process
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False
        self.previous_ball = (0,0)
        self.pred = 100  
    def update(self, scene_info):
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"
        
        ball_y = scene_info["ball"][1]
        platform_x = scene_info["platform"][0]
        

        if not self.ball_served:
            self.ball_served = True
            self.previous_ball = scene_info["ball"]
            command = "SERVE_TO_LEFT"
        else:
            self.pred = 100
            if self.previous_ball[1] - scene_info["ball"][1] < 0:
               self.pred = scene_info["ball"][0] + ((400- scene_info["ball"][1])//7 * (scene_info["ball"][0]-self.previous_ball[0]))                

            #預測落點調整　
            if self.pred > 400 : 
                self.pred -= 400
            elif self.pred > 200 and self.pred < 400:
                self.pred = 200 - (self.pred-200)
            elif self.pred >-200 and self.pred < 0:
                self.pred = abs(self.pred) 
            elif self.pred <-200 :
                self.pred = 200 - (abs(self.pred) - 200)

            if platform_x + 20   > self.pred :
                command = "MOVE_LEFT"
                #切球設定
                if ball_y > 380: 
                    command = "MOVE_RIGHT"
            elif platform_x + 20 < self.pred :
                command = "MOVE_RIGHT"
                #切球設定
                if ball_y > 380 :
                    command = "MOVE_LEFT"
            else :
                command = "NONE"
        #更新"前一點"座標=>"現在球"的座標
        self.previous_ball = scene_info["ball"]
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
