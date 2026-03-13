import React, { useState, useEffect, useRef } from 'react';
import { Bot, User, Send, MessageSquare, Loader, RefreshCw, AlertCircle } from 'lucide-react';
import { chatFlowHandler } from '../api'; 
import useThemeSettings from '../hooks/useThemeSettings'; 
import { useChat } from '../context/ChatContext'; 

const Chatbot = () => {
    const { settings } = useThemeSettings(); 
    const welcomeMessage = settings?.chatbot_welcome_message || "Hello! I'm XpertAI. Let's get you started.";

    const { isOpen, toggleChat } = useChat(); 
    
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [currentField, setCurrentField] = useState(null); 
    const [userName, setUserName] = useState(''); // Store user name
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    const startFlow = async (isRestart = false) => {
        setIsLoading(true);
        setUserName(''); // Reset name on restart
        try {
            const response = await chatFlowHandler({
                current_field: null, 
                answer: null
            });
            const data = response.data;

            const initialMessages = [
                { sender: 'bot', text: isRestart ? "Let's start over." : welcomeMessage },
                { sender: 'bot', text: data.next_question }
            ];

            setMessages(initialMessages);
            setCurrentField(data.next_field); 
        } catch (error) {
            console.error("Chatbot Error:", error);
            setMessages([{ sender: 'bot', text: 'Connection failed. Please try again.', isError: true }]);
        } finally {
            setIsLoading(false);
        }
    };

    // --- VALIDATION LOGIC ---
    const validateInput = (input, field) => {
        if (!input) return "Please enter a value.";

        // 1. Name Validation (No Numbers allowed)
        if (field === 'name') {
            if (/\d/.test(input)) {
                return "Names cannot contain numbers. Please enter a valid name.";
            }
            if (input.length < 2) {
                return "Name is too short.";
            }
        }

        // 2. Phone Validation (Must contain numbers, minimal length)
        if (field === 'phone') {
            const phoneRegex = /^[0-9+\-\s]+$/;
            if (!phoneRegex.test(input)) {
                return "Invalid format. Phone numbers should only contain digits.";
            }
            if (input.replace(/\D/g, '').length < 10) {
                return "Phone number is too short.";
            }
        }

        // 3. Email Validation
        if (field === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input)) {
                return "Please enter a valid email address.";
            }
        }

        return null; // No Error
    };

    const handleSend = async () => {
        const answer = inputValue.trim();
        
        // Prevent empty sending unless it's a generic message field
        if (!answer && currentField !== 'message') return;
        if (isLoading) return;

        // 1. Show User Message
        setMessages(prev => [...prev, { sender: 'user', text: answer }]);
        setInputValue('');

        // 2. RUN VALIDATION
        const errorMsg = validateInput(answer, currentField);
        
        if (errorMsg) {
            // Show error locally without calling API
            setTimeout(() => {
                setMessages(prev => [...prev, { sender: 'bot', text: errorMsg, isError: true }]);
                scrollToBottom();
            }, 500);
            return; // STOP execution here
        }

        // 3. CAPTURE NAME (If current field is name)
        if (currentField === 'name') {
            setUserName(answer);
        }

        // 4. Send to API
        setIsLoading(true);
        try {
            const response = await chatFlowHandler({
                current_field: currentField,
                answer: answer
            });
            const data = response.data;
            
            if (data.error) {
                setMessages(prev => [...prev, { sender: 'bot', text: data.error, isError: true }]);
            } else {
                let botResponseText = data.next_question;

                // 5. PERSONALIZED CLOSING
                // If chat is finished (no next_field) and we have a name, append it.
                if (!data.next_field && userName) {
                    botResponseText = `Thank you, ${userName}! ${botResponseText}`;
                } else if (!data.next_field && currentField === 'name') {
                    // Case where name was just entered as the last step
                    botResponseText = `Thank you, ${answer}! ${botResponseText}`;
                }

                setMessages(prev => [...prev, { sender: 'bot', text: botResponseText }]);
                
                if (data.next_field) {
                    setCurrentField(data.next_field); 
                } else {
                    setCurrentField(null); // Chat ended
                }
            }

        } catch (error) {
            console.error("Sending Error:", error);
            setMessages(prev => [...prev, { sender: 'bot', text: 'Error sending message. Please try again.', isError: true }]);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (isOpen && messages.length === 0) {
            startFlow();
        }
    }, [isOpen]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') handleSend();
    };

    return (
        <>
            <button
                className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-2xl hover:scale-110 transition z-50 hover:bg-blue-700"
                onClick={toggleChat}
            >
                <MessageSquare size={24} />
            </button>

            {isOpen && (
                <div className="fixed bottom-24 right-6 w-80 md:w-96 h-[500px] bg-white border border-gray-200 rounded-2xl shadow-2xl flex flex-col z-50 overflow-hidden font-sans animate-in slide-in-from-bottom-5 fade-in duration-300">
                    
                    {/* Header */}
                    <div className="bg-slate-900 text-white p-4 flex justify-between items-center shadow-md">
                        <div className="flex items-center gap-3">
                            <div className="relative">
                                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                                    <Bot size={18} />
                                </div>
                                <div className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-400 rounded-full border-2 border-slate-900"></div>
                            </div>
                            <div>
                                <h3 className="font-bold text-sm">XpertAI Assistant</h3>
                                <p className="text-[10px] text-slate-300">Online</p>
                            </div>
                        </div>
                        <div className="flex gap-2">
                             <button onClick={() => startFlow(true)} title="Restart" className="p-2 hover:bg-white/10 rounded-full transition"><RefreshCw size={16}/></button>
                             <button onClick={toggleChat} title="Close" className="p-2 hover:bg-red-500/20 hover:text-red-300 rounded-full transition">&times;</button>
                        </div>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                                {msg.sender === 'bot' && (
                                    <div className="w-6 h-6 bg-slate-200 rounded-full flex items-center justify-center mr-2 mt-1 flex-shrink-0">
                                        <Bot size={14} className="text-slate-600"/>
                                    </div>
                                )}
                                <div className={`max-w-[80%] p-3 rounded-2xl text-sm leading-relaxed shadow-sm ${
                                    msg.sender === 'user' 
                                    ? 'bg-blue-600 text-white rounded-tr-none' 
                                    : msg.isError 
                                        ? 'bg-red-50 text-red-600 border border-red-100 rounded-tl-none flex items-start gap-2'
                                        : 'bg-white text-slate-800 border border-slate-200 rounded-tl-none'
                                }`}>
                                    {msg.isError && <AlertCircle size={16} className="mt-0.5 flex-shrink-0"/>}
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="bg-white border border-slate-200 px-4 py-3 rounded-2xl rounded-tl-none shadow-sm flex gap-1">
                                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></div>
                                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="p-3 bg-white border-t border-slate-100">
                        <div className="flex gap-2 items-center bg-slate-100 p-1.5 rounded-xl border border-slate-200 focus-within:border-blue-400 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
                            <input
                                type="text"
                                className="flex-1 p-2 bg-transparent border-0 outline-none text-sm text-slate-700 placeholder:text-slate-400"
                                placeholder={currentField ? `Type your ${currentField}...` : "Chat ended."}
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyDown={handleKeyDown}
                                disabled={!currentField || isLoading}
                                autoComplete="off"
                            />
                            <button
                                className={`p-2 rounded-lg transition-all duration-200 ${
                                    !currentField || isLoading || !inputValue.trim()
                                    ? 'bg-slate-200 text-slate-400 cursor-not-allowed' 
                                    : 'bg-blue-600 text-white hover:bg-blue-700 shadow-md'
                                }`}
                                onClick={handleSend}
                                disabled={!currentField || isLoading || !inputValue.trim()}
                            >
                                <Send size={18} />
                            </button>
                        </div>
                        {currentField && (
                            <p className="text-[10px] text-slate-400 text-center mt-2">
                                Please provide a valid {currentField}.
                            </p>
                        )}
                    </div>
                </div>
            )}
        </>
    );
};

export default Chatbot;