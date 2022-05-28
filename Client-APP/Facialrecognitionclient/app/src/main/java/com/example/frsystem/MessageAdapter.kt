package com.example.frsystem

import android.annotation.SuppressLint
import android.content.Context
import android.text.Layout
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView
import com.example.frsystem.databinding.MessageItemBinding

class MessageAdapter(val context: Context, val messageList: ArrayList<MessageData>) : BaseAdapter() {
    override fun getCount(): Int {
        return messageList.size
    }

    override fun getItem(position: Int): Any {
        return messageList[position]
    }

    override fun getItemId(position: Int): Long {
        return 0
    }

    @SuppressLint("ViewHolder", "InflateParams")
    override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
        val view: View = LayoutInflater.from(context).inflate(R.layout.message_item,null)

        val msg = view.findViewById<TextView>(R.id.tvMessage)
        val dateTime = view.findViewById<TextView>(R.id.tvDateTime)

        val message = messageList[position]
        msg.text = message.msg
        dateTime.text = message.dataTime

        return view
    }

}