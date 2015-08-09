#include "capture.h"
#include "clientClass.h"
#include <stdio.h>
#include <pthread.h>

using namespace std;

class ThreadClass {
private:
  pthread_t thread_handler;      // スレッドハンドラ
  pthread_mutex_t mutex; // ミューテックス(排他処理で優先権を決めるやつ)

public:
  ThreadClass(){
  }

  // ランチャ
  //
  static void* executeLauncher(void* args){
    std::cout << "executeLauncher" << std::endl;
    // 引数に渡されたインスタンスを無理やりキャストして、インスタンスメソッドを実行
    reinterpret_cast<ThreadTest*>(args)->execute();
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
		     &ThreadTest::executeLauncher,         // スレッドにできるのは、static なメソッドや関数のみ
		     this
						);
    }
  }

  // スレッドで実行したいインスタンスメソッド
  //
  virtual void execute(){
    while(1){
      pthread_testcancel();                 // キャンセル要求が来ていたらここで終了
      pthread_mutex_lock(&(this->mutex));   // 優先権を保持するまで待機
      sleep(10);                            // mutex_lock が判るように sleep を入れる
      pthread_mutex_unlock(&(this->mutex)); // 優先権を破棄
      sleep(1);
    }
  }

  // デストラクタ
  // * 終了時に、スレッドにキャンセル要求を投げる
  //
  ~ThreadClass(){
    std::cout << "destructor start" << std::endl;
    pthread_cancel(this->thread_handler);     // スレッドにキャンセル要求を投げる
    pthread_join(this->thread_handler, NULL); // スレッドが終了するまで待機
    std::cout << "destructor end" << std::endl;
  }
};

class SendThread:public ThreadClass{

public:

  cv::Mat frame;

  SendThread(){
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


  void execute(){

    vector<uchar> buff;
    vector<int> param;
    param.push_back(CV_IMWRITE_JPEG_QUALITY);
    param.push_back(95);

    string LOCALHOST="127.0.0.1";//ローカルホストのIPアドレス
    int PORT=12345;//ポート番号

    while(1){
      pthread_testcancel();                 // キャンセル要求が来ていたらここで終了
      TcpClient client;
      if(!client.Init(LOCALHOST,PORT)){
	perror("connect server is failed.\n");
	return;
      }

      pthread_mutex_lock(&(this->mutex));   // 優先権を保持するまで待機
      cv::imencode(".jpg",frame,buff,param);
      pthread_mutex_unlock(&(this->mutex)); // 優先権を破棄
      
      vector<char> data;
      vector<uchar>::iterator iterator = buff.begin(); 
      while(iterator != buff.end()){
	data.push_back(static_cast<char>(*iterator));
	iterator++;
      }
      
      printf("data size is %lu\n",data.size());
      int nSend=client.Write(data);//データ受信
      
      printf("send size : %d\n",nSend);

    }
  }

};

class CaptureClass:public ThreadClass{
  
  public CaptureClass(){
  }

  void execute(){

    SendThread *st = new SendThread();
    int camera_id = 0;
    cv::VideoCapture cap(camera_id);
    ostringstream oss;

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

    delete(st);

  }
}
