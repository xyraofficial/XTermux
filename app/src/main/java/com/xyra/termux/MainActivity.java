package com.xyra.termux;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.LinearLayout;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import com.google.android.material.card.MaterialCardView;

public class MainActivity extends AppCompatActivity {
    
    private TextView featureTitle;
    private TextView featureDescription;
    private LinearLayout featureContentContainer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            setContentView(R.layout.activity_main);
                    
            Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
            if (toolbar != null) {
                setSupportActionBar(toolbar);
                if (getSupportActionBar() != null) {
                    getSupportActionBar().setDisplayShowTitleEnabled(false);
                }
            }

            featureTitle = (TextView) findViewById(R.id.feature_title);
            featureDescription = (TextView) findViewById(R.id.feature_description);
            featureContentContainer = (LinearLayout) findViewById(R.id.feature_content_container);

            setupCard(R.id.card_info, "Source Info", "Termux official sources are hosted on GitHub.\n\n• Main app: github.com/termux/termux-app\n• Packages: github.com/termux/termux-packages\n• Wiki: wiki.termux.com");
            setupCard(R.id.card_package, "Package Search", "Search and manage packages effectively:\n\n• pkg search <query>\n• pkg install <package>\n• pkg list-all\n• pkg files <package>");
            setupCard(R.id.card_setup, "Setup Guide", "Essential first steps:\n\n1. pkg update && pkg upgrade\n2. termux-setup-storage\n3. pkg install build-essential\n4. pkg install termux-api\n5. termux-chroot (optional)");
            setupCard(R.id.card_storage, "Storage Management", "Manage your Termux storage:\n\n• termux-setup-storage (Access internal storage)\n• du -h (Check disk usage)\n• df -h (Check filesystem space)\n• rm -rf ~/.thumbnails (Clear cache)");
            setupCard(R.id.card_network, "Network Tools", "Network utility commands:\n\n• ifconfig (Check IP address)\n• ping <host> (Test connectivity)\n• netstat -tupln (Active connections)\n• nmap <target> (Network scan)");
            setupCard(R.id.card_system, "System Information", "Check device hardware & software:\n\n• uname -a (Kernel version)\n• lscpu (CPU architecture)\n• free -h (RAM usage)\n• uptime (System runtime)\n• getprop (Android properties)");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void setupCard(int id, final String title, final String desc) {
        final MaterialCardView card = (MaterialCardView) findViewById(id);
        if (card != null) {
            card.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(final View v) {
                    v.animate().scaleX(0.95f).scaleY(0.95f).setDuration(100).withEndAction(new Runnable() {
                        @Override
                        public void run() {
                            v.animate().scaleX(1.0f).scaleY(1.0f).setDuration(100);
                            showFeature(title, desc);
                        }
                    });
                }
            });
        }
    }

    public void hideFeature(View view) {
        if (featureContentContainer != null) {
            featureContentContainer.animate()
                .alpha(0f)
                .translationY(50f)
                .setDuration(200)
                .withEndAction(new Runnable() {
                    @Override
                    public void run() {
                        featureContentContainer.setVisibility(View.GONE);
                    }
                });
        }
    }

    private void showFeature(String title, String description) {
        if (featureTitle != null) featureTitle.setText(title);
        if (featureDescription != null) featureDescription.setText(description);
        if (featureContentContainer != null) {
            featureContentContainer.setVisibility(View.VISIBLE);
            featureContentContainer.setAlpha(0f);
            featureContentContainer.setTranslationY(50f);
            featureContentContainer.animate()
                .alpha(1f)
                .translationY(0f)
                .setDuration(300)
                .start();
        }
    }
}
