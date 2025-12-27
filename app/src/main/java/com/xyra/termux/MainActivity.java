package com.xyra.termux;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import com.google.android.material.card.MaterialCardView;

public class MainActivity extends AppCompatActivity {
    
    private TextView featureTitle;
    private TextView featureDescription;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
                
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        if (getSupportActionBar() != null) {
            getSupportActionBar().setDisplayShowTitleEnabled(false);
        }

        featureTitle = (TextView) findViewById(R.id.feature_title);
        featureDescription = (TextView) findViewById(R.id.feature_description);

        MaterialCardView cardInfo = (MaterialCardView) findViewById(R.id.card_info);
        MaterialCardView cardPackage = (MaterialCardView) findViewById(R.id.card_package);
        MaterialCardView cardSetup = (MaterialCardView) findViewById(R.id.card_setup);

        if (cardInfo != null) {
            cardInfo.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    showFeature("Source Info", "Termux official sources are hosted on GitHub. \nMain repo: github.com/termux/termux-app \nPackages: github.com/termux/termux-packages");
                }
            });
        }

        if (cardPackage != null) {
            cardPackage.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    showFeature("Package Search", "Use 'pkg search <name>' in Termux. \nCommon packages: \n- python\n- git\n- vim\n- curl");
                }
            });
        }

        if (cardSetup != null) {
            cardSetup.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    showFeature("Setup Guide", "1. pkg update && pkg upgrade\n2. termux-setup-storage\n3. pkg install build-essential\n4. pkg install termux-api");
                }
            });
        }
    }

    private void showFeature(String title, String description) {
        if (featureTitle != null) featureTitle.setText(title);
        if (featureDescription != null) featureDescription.setText(description);
    }
}