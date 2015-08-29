#include "cv.h"
#include "highgui.h"
#include "ctype.h"
#include <opencv2/highgui/highgui.hpp>
#include <unistd.h>
#include <iostream>
#include <iomanip>
#include <stdio.h>
#include <pthread.h>
#include <time.h>
#include <sys/time.h>
#include "clientClass.h"

#ifndef CAPTURE_H
#define CAPTURE_H

using namespace std;

class ThreadClass {
protected:
  pthread_t thread_handler;      // スレッドハンドラ
  pthread_mutex_t mutex; // ミューテックス(排他処理で優先権を決めるやつ)

public:
  ThreadClass(){
    printf("testclass\n");
  }

  // ランチャ
  //
  static void* executeLauncher(void* args){
    cout << "executeLauncher" << std::endl;
    // 引数に渡されたインスタンスを無理やりキャストして、インスタンスメソッドを実行
    reinterpret_cast<ThreadClass*>(args)->execute();
    return (void*)NULL;
  }

  // スレッド開始
  void threadStart(){
    if ((this->thread_handler) == NULL){
      std::cout << "threadStart" << std::endl;
      pthread_mutex_init(&(this->mutex), NULL); // ミューテックスの初期化
      pthread_create(                           // スレッドの生成
		     &(this->thread_handler),
		     NULL,
		     &ThreadClass::executeLauncher,         // スレッドにできるのは、static なメソッドや関数のみ
		     this
						);
    }
  }

  // スレッドで実行したいインスタンスメソッド
  //
  void execute(){
    run();
  }

  virtual void run(){
    while(1){
      pthread_testcancel();                 // キャンセル要求が来ていたらここで終了
      pthread_mutex_lock(&(this->mutex));   // 優先権を保持するまで待機
      std::cout << "test\n" << endl;
      pthread_mutex_unlock(&(this->mutex)); // 優先権を破棄
      sleep(1);
    }
  }

  // デストラクタ
  // * 終了時に、スレッドにキャンセル要求を投げる
  //
  virtual ~ThreadClass(){
    std::cout << "destructor start" << std::endl;
    pthread_cancel(this->thread_handler);     // スレッドにキャンセル要求を投げる
    pthread_join(this->thread_handler, NULL); // スレッドが終了するまで待機
    std::cout << "destructor end" << std::endl;
  }
};

class SendThread : public ThreadClass{

public:

  cv::Mat frame;

  SendThread(){
    printf("sendthread\n");
  }

  ~SendThread(){
  }

  // data に値を挿入
  // * execute が優先権を保持している間は待機する
  //
  void setData(cv::Mat fr){
    pthread_mutex_lock(&(this->mutex));   // 優先権を保持するまで待機
    frame = fr.clone();
    pthread_mutex_unlock(&(this->mutex)); // 優先権を破棄
  }
  cv::Mat getData(){ return frame; }

  //現在時刻取得
  static string getTime(){
    ostringstream oss;
    struct tm *tmp;
    struct timeval tv;

    gettimeofday(&tv,NULL);
    tmp=localtime(&tv.tv_sec);
    /*
    sprintf(oss.,"%04d-%02d-%02d %02d:%02d:%02d.%3d\n",
	   tmp->tm_year + 1900, tmp->tm_mon + 1,
	   tmp->tm_mday, tmp->tm_hour,
	   tmp->tm_min, tmp->tm_sec,
	   tv.tv_usec/1000);
    */
    oss << setw(4) << setfill('0') << tmp->tm_year + 1900 << "-" //year
	<< setw(2) << setfill('0') << tmp->tm_mon + 1 << "-" //month
	<< setw(2) << setfill('0') << tmp->tm_mday << " "   //day
	<< setw(2) << setfill('0') << tmp->tm_hour << ":" //hour
	<< setw(2) << setfill('0') << tmp->tm_min << ":" //minute
	<< setw(2) << setfill('0') << tmp->tm_sec << "." //second
	<< setw(3) << tv.tv_usec/1000;  //milisecond

    return oss.str();
  }


  void run(){

    vector<uchar> buff;
    vector<int> param;
    param.push_back(CV_IMWRITE_JPEG_QUALITY);
    param.push_back(95);

    string LOCALHOST="127.0.0.1";//ローカルホストのIPアドレス
    int PORT=12345;//ポート番号

    while(1){
      pthread_testcancel();                 // キャンセル要求が来ていたらここで終了
      if(frame.empty()) continue;

      TcpClient client;
      if(!client.Init(LOCALHOST,PORT)){
	perror("connect server is failed.\n");
	return;
      }

      pthread_mutex_lock(&(this->mutex));   // 優先権を保持するまで待機
      cv::imencode(".jpg",frame,buff,param); //convert from mat to jpg
      pthread_mutex_unlock(&(this->mutex)); // 優先権を破棄
      
      vector<char> data;
      cout << "getTime:" << getTime() << endl;
      string nowtime = getTime();
      string::iterator timestamp_iterator = nowtime.begin();

      for(; timestamp_iterator != nowtime.end() ; timestamp_iterator++){
	data.push_back(*timestamp_iterator);
      }

      data.push_back('\t');  //character for split timestamp and image data

      vector<uchar>::iterator image_iterator = buff.begin(); 
      for(;image_iterator != buff.end();image_iterator++){
	data.push_back(static_cast<char>(*image_iterator));
      }
      
      printf("data size is %lu\n",data.size());
      int nSend=client.Write(data);//データ送信
      
      printf("send size : %d\n",nSend);

      sleep(5);

    }
  }

};


/*
Captureもクラスを使ってやりたかったが、
threadからvideoCaptureが動かないというなぞバグにより断念
*/
class CaptureThread : public ThreadClass{

 public:
  CaptureThread(){
    printf("capturethread\n");
  }

  ~CaptureThread(){
  }
  
  void run(){

    SendThread *st = new SendThread();

    int camera_id = 0;
    cv::VideoCapture cap(camera_id);
    ostringstream oss;
    cv::Mat frame;
    if(!cap.isOpened()){
      perror("cameara open error.\n");
      return;
    }

    cap.set(CV_CAP_PROP_FPS, 30.0);
    cv::namedWindow("capture",cv::WINDOW_AUTOSIZE);

    st->threadStart();

    while(1){
      pthread_testcancel();                 // キャンセル要求が来ていたらここで終了
      cap >> frame;
      if(frame.empty()) break;

      st->setData(frame);

      cv::imshow("capture",frame);
      if(cv::waitKey(30) >= 0) break;

    }

    delete st;

  }

};

#endif
