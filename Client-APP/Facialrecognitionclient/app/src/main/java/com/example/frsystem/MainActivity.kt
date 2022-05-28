package com.example.frsystem

import android.annotation.SuppressLint
import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Message
import android.util.Log
import android.widget.Toast
import com.example.frsystem.databinding.ActivityMainBinding
import org.eclipse.paho.android.service.MqttAndroidClient
import org.eclipse.paho.client.mqttv3.*
import java.text.SimpleDateFormat

class MainActivity : AppCompatActivity() {
    lateinit var mqttAndroidClient:MqttAndroidClient
    lateinit var binding: ActivityMainBinding
    lateinit var token: IMqttToken
    var msgList = arrayListOf<MessageData>()
    lateinit var adapter:MessageAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // view binding 설정
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // adapter 설정
        adapter = MessageAdapter(this, msgList)
        binding.lvMessages.adapter = adapter

        binding.btnContact.setOnClickListener {
            val address = binding.etAddress.text.toString()
            val port = binding.etPort.text.toString()
            if (address != "" && port != ""){
                mqttAndroidClient = MqttAndroidClient(this, "tcp://$address:${port.toInt()}", MqttClient.generateClientId())
            }else{
                Toast.makeText(this, "주소와 포트번호를 채우세요", Toast.LENGTH_SHORT).show()
            }

            try{
                token = mqttAndroidClient.connect(getMqttConnectionOption())
                token.actionCallback = object: IMqttActionListener{
                    override fun onSuccess(asyncActionToken: IMqttToken?) {
//                        mqttAndroidClient.setBufferOpts(getDisconnectedBufferOptions())
                        binding.tvIsConnected.text = "연결에 성공했습니다."
                        binding.tvIsConnected.setTextColor(Color.GREEN)

                        mqttAndroidClient.setCallback(object: MqttCallback{
                            override fun connectionLost(cause: Throwable?) {}
                            @SuppressLint("SimpleDateFormat")
                            override fun messageArrived(topic: String?, message: MqttMessage?) {
                                if (topic.equals("jhm")){
                                    if(message != null) {
                                        val msg = String(message.payload)
                                        val currentTime = System.currentTimeMillis()
                                        val dataFormat = SimpleDateFormat("yy-MM-dd HH:mm:ss")
                                        val dateTime = dataFormat.format(currentTime)
                                        msgList.add(MessageData(msg, dateTime))
                                        adapter.notifyDataSetChanged()
                                    }
                                }
                            }
                            override fun deliveryComplete(token: IMqttDeliveryToken?) {}
                        })
                        try{
                            mqttAndroidClient.subscribe("jhm", 0)
                        }catch (e: MqttException){
                            e.printStackTrace()
                        }
                    }

                    override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                        binding.tvIsConnected.text = "연결에 실패했습니다."
                        binding.tvIsConnected.setTextColor(Color.RED)
                    }
                }
            }catch (e: MqttException){
                e.printStackTrace()
            }
        }

    }

    fun getMqttConnectionOption() : MqttConnectOptions{
        val mqttConnectOptions = MqttConnectOptions()
        mqttConnectOptions.isCleanSession = false
        mqttConnectOptions.isAutomaticReconnect = true
        mqttConnectOptions.setWill("aaa","I am going offline".toByteArray(),1,true)
        return mqttConnectOptions
    }

    fun getDisconnectedBufferOptions():DisconnectedBufferOptions{
        val disconnectedBufferOptions = DisconnectedBufferOptions()
        disconnectedBufferOptions.isBufferEnabled = true
        disconnectedBufferOptions.bufferSize = 100
        disconnectedBufferOptions.isPersistBuffer = true
        disconnectedBufferOptions.isDeleteOldestMessages = false
        return disconnectedBufferOptions

    }
}

