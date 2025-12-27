package com.xyra.termux;

import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

public class MainActivity extends AppCompatActivity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
                
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayShowTitleEnabled(false);
        }

        EditText searchInput = findViewById(R.id.search_input);
        Button btnSearch = findViewById(R.id.btn_search);

        btnSearch.setOnClickListener(v -> {
            String query = searchInput.getText().toString();
            if (!query.isEmpty()) {
                Toast.makeText(this, "Searching for: " + query, Toast.LENGTH_SHORT).show();
                // Logic for package search would go here
            } else {
                Toast.makeText(this, "Please enter a package name", Toast.LENGTH_SHORT).show();
            }
        });
    }
}