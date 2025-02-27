package com.pushpak.tissquiz;

import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.List;

public class StartingScreenActivity extends AppCompatActivity {
    private static final int REQUEST_CODE_QUIZ = 1;
    public static final String EXTRA_CATEGORY_ID = "extraCategoryID";
    public static final String EXTRA_CATEGORY_NAME = "extraCategoryName";
    public static final String EXTRA_DIFFICULTY = "extraDifficulty";

    public static final String SHARED_PREFS = "sharedPrefs";
    public static final String KEY_HIGHSCORE = "keyHighscore";
    public static final String KEY_HIGHUSER = "keyHighUser";
    private TextView textViewHighscore;
    private TextView textViewUser;
    private Spinner spinnerDifficulty;
    private Spinner spinnerCategory;
    private int highscore;
    private static String user;
    private static String highScoreUser = "";
    private long backPressedTime;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_starting_screen);

        textViewHighscore = findViewById(R.id.text_view_highscore);
        textViewUser = findViewById(R.id.textViewUser);

        Intent intent1 = getIntent();
       user = intent1.getStringExtra("user");

       textViewUser.setText("Student Name : " + user);
        spinnerDifficulty= findViewById(R.id.spinner_difficulty);
        spinnerCategory= findViewById(R.id.spinner_category);



        loadCategories();
        loadDifficultyLevels();
        loadHighScore();

        Button buttonStartQuiz = findViewById(R.id.button_start_quiz);
        buttonStartQuiz.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
        startQuiz();
            }
        });


    }

    private void startQuiz(){
        Category selectedCategory = (Category) spinnerCategory.getSelectedItem();
        int categoryID = selectedCategory.getId();
        String categoryName = selectedCategory.getName();
        String diff = spinnerDifficulty.getSelectedItem().toString();

        Intent intent = new Intent(StartingScreenActivity.this,QuizActivity.class);
        intent.putExtra(EXTRA_CATEGORY_ID, categoryID);
        intent.putExtra(EXTRA_CATEGORY_NAME, categoryName);
        intent.putExtra(EXTRA_DIFFICULTY, diff);

        startActivityForResult(intent, REQUEST_CODE_QUIZ );

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode ==  REQUEST_CODE_QUIZ){
            if(resultCode == RESULT_OK){
                int score = data.getIntExtra(QuizActivity.EXTRA_SCORE, 0);
                if(score > highscore){
                    updateScore(score);
                }
            }
        }
    }


    private void loadCategories(){
        QuizDbHelper dbHelper = QuizDbHelper.getInstance(this);
        List<Category> categories = dbHelper.getAllCategories();

        ArrayAdapter<Category> adapterCategories = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, categories);
        adapterCategories.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerCategory.setAdapter(adapterCategories);
    }

    private void loadDifficultyLevels(){
        String[] difficultyLevels = Question.getAllDifficultyLevels();
        ArrayAdapter<String> adapterDifficulty = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item, difficultyLevels);
        adapterDifficulty.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerDifficulty.setAdapter(adapterDifficulty);
    }

    //Load highscore from SharedPrefs
    private void loadHighScore(){
        SharedPreferences prefs = getSharedPreferences(SHARED_PREFS,MODE_PRIVATE);
        highscore = prefs.getInt(KEY_HIGHSCORE, 0);
        highScoreUser = prefs.getString(KEY_HIGHUSER,"");
        if(highScoreUser.equals("")){
            textViewHighscore.setText("No Highscore Yet. Come on, let's start !");
        }else {
            textViewHighscore.setText("All Time Highscore: " + highscore + " (" + highScoreUser + ")");
        }
    }

    public void MyWeb(View view)
    {
        openUrl("http://wwww.google.com");


    }

    public void openUrl(String url)
    {
        Uri uri = Uri.parse(url);
        Intent launchWeb=new Intent(Intent.ACTION_VIEW,uri);
        startActivity(launchWeb);


    }

    private void updateScore(int highscoreNew){
        highscore = highscoreNew;
        highScoreUser = user;
        textViewHighscore.setText("All Time Highscore: " + highscore + " ("+highScoreUser+")");

        //Save value in Shared Prefs
        SharedPreferences prefs = getSharedPreferences(SHARED_PREFS,MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();
        editor.putInt(KEY_HIGHSCORE, highscore);
        editor.putString(KEY_HIGHUSER, highScoreUser);

        editor.apply();
    }

    @Override
    public void onBackPressed() {
        if(backPressedTime + 2000 > System.currentTimeMillis()){
            LoginActivity.mTextPassword.setText("");
            LoginActivity.mTextUsername.setText("");
            LoginActivity.mTextPassword.clearFocus();
            finish();
        }else{
            Toast.makeText(this, "Press Back Again To Go Back to Login", Toast.LENGTH_SHORT).show();
        }
        backPressedTime = System.currentTimeMillis();

    }

}
