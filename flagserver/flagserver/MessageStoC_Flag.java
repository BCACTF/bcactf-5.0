package flagserver;

public class MessageStoC_Flag extends Message {
    public String flag;

    public MessageStoC_Flag(String flag) {
        this.flag = flag;
    }

    public String toString() {
        return "Flag: " + flag;
    }

}