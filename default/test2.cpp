#include "cv.h"
#include "highgui.h"
#include "ctype.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

int
main (int argc, char **argv)
{

  int camera_id = 0;
  cv::VideoCapture cap(camera_id);

  if(!cap.isOpened()) return -1;

  cap.set(CV_CAP_PROP_FPS, 30.0);

  cv::namedWindow("capture",cv::WINDOW_AUTOSIZE);

  cv::Mat frame;

  for(;;){
    cap >> frame;
    if(frame.empty()) break;
    cv::imshow("capture",frame);

    if(cv::waitKey(30) >= 0) break;
  }


  return 0;
}

