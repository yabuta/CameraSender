#include "cv.h"
#include "highgui.h"
#include "ctype.h"
#include <opencv2/highgui/highgui.hpp>
#include <unistd.h>
#include <iostream>

#include "sendData.h"
#include "clientClass.h"

using namespace std;

int
main (int argc, char **argv)
{

  int camera_id = 0;
  cv::VideoCapture cap(camera_id);
  ostringstream oss;

  TcpClient tclient;
  string LOCALHOST="127.0.0.1";//ローカルホストのIPアドレス
  int PORT=50001;//ポート番号
  //client.Init(LOCALHOST,PORT);

  if(!cap.isOpened()) return -1;

  cap.set(CV_CAP_PROP_FPS, 30.0);

  cv::namedWindow("capture",cv::WINDOW_AUTOSIZE);

  cv::Mat frame;
  
  for(int i=0 ;i < 100 ;i++){
    cap >> frame;
    if(frame.empty()) break;

    oss << "picture/" << "test" << i << ".jpg";    
    cv::imwrite(oss.str(),frame);
    oss.str("");
    oss.clear(stringstream::goodbit);

    int frameSize =  frame.total()*frame.elemSize();
    vector<char> data;
    for(int i=0; i<frameSize ; i++){
      data.push_back(*reinterpret_cast<char*>(&(frame.data[i])));
    }

    printf("data size is %lu\n",data.size());
    //int nSend=tcp.Read(data);//データ受信

    cv::imshow("capture",frame);
    if(cv::waitKey(30) >= 0) break;

    sleep(10);

  }


  return 0;
}

