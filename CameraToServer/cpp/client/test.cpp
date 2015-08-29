#include "capture.h"
#include <pthread.h>

using namespace std;

bool capture_stop = false;

void* thread_func(void *arg){

  SendThread *st = new SendThread();
  st->threadStart();

  int camera_id = 0;
  cv::VideoCapture cap(camera_id);
  if(!cap.isOpened()){
    perror("cameara open error.\n");
    return 0;
  }

  cv::Mat frame;
  cap.set(CV_CAP_PROP_FPS, 30.0);
  cv::namedWindow("capture",cv::WINDOW_AUTOSIZE);

  while(1){

    if(capture_stop) break;

    cap >> frame;
    if(frame.empty()){
      perror("capture frame is empty.\n");
      break;
    }
    st->setData(frame);
    
    cv::imshow("capture",frame);
    if(cv::waitKey(30) >= 0) break;
    
  }

  delete st;

  return (void*)NULL;
}

int
main (int argc, char **argv)
{
  
  pthread_t th;
  pthread_create(&th,NULL,&thread_func,NULL);
  
  char c;
  printf("input some character for end.\n");
  scanf("%c",&c);

  capture_stop = true;

  pthread_join(th,NULL);

  return 0;
}

