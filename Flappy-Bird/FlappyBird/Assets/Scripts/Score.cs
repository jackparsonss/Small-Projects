using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public static class Score
{

    public static void Start()
    {        
        Bird.GetInstance().OnDied += Score_BirdDied;      
    }

    private static void Score_BirdDied(object sender, System.EventArgs e)
    {
        TrySetNewHighscore(Level.GetInstance().GetPipesPasedCount());
    }

    public static int GetHighscore()
    {
        return PlayerPrefs.GetInt("highscore");
    }



    public static bool TrySetNewHighscore(int score)
    {
        int currentHighscore = GetHighscore();
        if (score > currentHighscore)
        {
            PlayerPrefs.SetInt("highscore", score);
            PlayerPrefs.Save();
            return true;
        }
        else
        {
            return false;
        }        
    }

    public static void ResetHighscore()
    {
        PlayerPrefs.SetInt("highscore", 0);
        PlayerPrefs.Save();

    }
}
