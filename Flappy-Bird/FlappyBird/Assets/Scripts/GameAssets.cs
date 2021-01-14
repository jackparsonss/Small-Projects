using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameAssets : MonoBehaviour
{
    private static GameAssets instance;

    public static GameAssets GetInstance()
    {
        return instance;
    }

    private void Awake()
    {
        instance = this;
    }


    public Sprite pipeHeadSprite;

    public Transform pfPipeHead;
    public Transform pfPipeBody;
    public Transform pfGround;
    public Transform pfClouds_1;
    public Transform pfClouds_2;
    public Transform pfClouds_3;

    public SoundAudioClip[] soundAudioClipArray;

    [Serializable]
    public class SoundAudioClip
    {
        public SoundManager.Sound sound;
        public AudioClip audioClip;
    }
}
