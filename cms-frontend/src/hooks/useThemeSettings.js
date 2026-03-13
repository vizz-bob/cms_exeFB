// src/hooks/useThemeSettings.js

import { useState, useEffect } from 'react';
// Assuming this function is correctly defined in src/api/index.js
import { getThemeSettings } from '../api'; 

/**
 * Fetches the active theme settings and provides them.
 * Chatbot uses this to get its configurable welcome message.
 */
const useThemeSettings = () => {
    const [settings, setSettings] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSettings = async () => {
            try {
                // getThemeSettings function ko call karein (jo niche diya gaya hai)
                const response = await getThemeSettings(); 
                // Response.data mein ThemeSetting ka object hona chahiye
                setSettings(response.data); 
            } catch (err) {
                console.error("Error fetching theme settings:", err);
                setError(err);
                // Fallback setting for Chatbot welcome message
                setSettings({ 
                    chatbot_welcome_message: "System Error: Cannot load chat configuration.",
                }); 
            } finally {
                setLoading(false);
            }
        };

        fetchSettings();
    }, []);

    return { settings, loading, error };
};

export default useThemeSettings;