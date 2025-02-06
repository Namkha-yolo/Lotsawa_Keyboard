import 'package:flutter/material.dart';

void main() {
  runApp(const LotsawaKeyboardApp());
}

class LotsawaKeyboardApp extends StatelessWidget {
  const LotsawaKeyboardApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lotsawa Keyboard',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const KeyboardScreen(),
    );
  }
}

class KeyboardScreen extends StatefulWidget {
  const KeyboardScreen({Key? key}) : super(key: key);

  @override
  _KeyboardScreenState createState() => _KeyboardScreenState();
}

class _KeyboardScreenState extends State<KeyboardScreen> {
  String inputText = ''; // Holds the input text
  
  // Sample QWERTY keyboard layout
  final List<String> keyboardKeys = [
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ', 'Back'
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Lotsawa Keyboard')),
      body: Column(
        children: [
          // Input Text Area
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: TextEditingController(text: inputText),
              maxLines: 3,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Romanized Input',
              ),
              onChanged: (text) {
                setState(() {
                  inputText = text;
                });
              },
            ),
          ),

          // QWERTY Keyboard Grid
          Expanded(
            child: GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 10, // Adjust for proper QWERTY layout
                crossAxisSpacing: 4.0,
                mainAxisSpacing: 4.0,
              ),
              itemCount: keyboardKeys.length,
              itemBuilder: (context, index) {
                return ElevatedButton(
                  onPressed: () {
                    setState(() {
                      if (keyboardKeys[index] == 'Back') {
                        inputText = inputText.isNotEmpty
                            ? inputText.substring(0, inputText.length - 1)
                            : inputText;
                      } else {
                        inputText += keyboardKeys[index];
                      }
                    });
                  },
                  child: Text(keyboardKeys[index]),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
