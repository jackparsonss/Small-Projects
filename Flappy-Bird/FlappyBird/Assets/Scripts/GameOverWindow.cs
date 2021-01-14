﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using CodeMonkey.Utils;

public class GameOverWindow : MonoBehaviour
{
    private Text scoreText;
    private Text highscoreText;

    private void Awake()
    {
        scoreText = transform.Find("ScoreText").GetComponent<Text>();
        highscoreText = transform.Find("highscoreText").GetComponent<Text>();

        transform.Find("retryBtn").GetComponent<Button_UI>().ClickFunc = () => { Loader.Load(Loader.Scene.GameScene);  };
        transform.Find("retryBtn").GetComponent<Button_UI>().AddButtonSounds();

        transform.Find("mainMenuBtn").GetComponent<Button_UI>().ClickFunc = () => { Loader.Load(Loader.Scene.MainMenu); };
        transform.Find("mainMenuBtn").GetComponent<Button_UI>().AddButtonSounds();

    }

    private void Start()
    {
        Bird.GetInstance().OnDied += Bird_OnDied;
        Hide();
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Loader.Load(Loader.Scene.GameScene);
        }
    }

    private void Bird_OnDied(object sender, System.EventArgs e)
    {
        scoreText.text = Level.GetInstance().GetPipesPasedCount().ToString();

        if (Level.GetInstance().GetPipesPasedCount() >= Score.GetHighscore())
        { 
            highscoreText.text = "NEW HIGHSCORE!"; 
        }
        else
        {
            highscoreText.text = "HIGHSCORE: " + Score.GetHighscore();
        }

        
        Show();
    }

    private void Hide()
    {
        gameObject.SetActive(false);
    }

    private void Show()
    {
        gameObject.SetActive(true);
    }
}
