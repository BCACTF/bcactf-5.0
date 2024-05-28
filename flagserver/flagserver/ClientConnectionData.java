package flagserver;

import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.Socket;

public class ClientConnectionData {
    private Socket socket;
    private ObjectInputStream input;
    private ObjectOutputStream out;
    private String name;

    public ClientConnectionData(Socket socket, ObjectInputStream input, ObjectOutputStream out, String name) {
        this.socket = socket;
        this.input = input;
        this.out = out;
        this.name = name;
    }

    public Socket getSocket() {
        return socket;
    }

    public void setSocket(Socket socket) {
        this.socket = socket;
    }

    public ObjectInputStream getInput() {
        return input;
    }

    public void setInput(ObjectInputStream input) {
        this.input = input;
    }

    public ObjectOutputStream getOut() {
        return out;
    }

    public void setOut(ObjectOutputStream out) {
        this.out = out;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    
}
