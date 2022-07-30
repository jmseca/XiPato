/*
Maybe I can do this in Python, I dont think i need this
I'll keep it here anyway, for a possible future enlightening
*/


int main() {
    char stop = 0;
    char err[50];
    int pid, status;
    while (!stop) {
        // Scrape OLX, FB ads
        pid = fork();
        if (pid<0){
            stop = 1;
            break;
        }
        if (pid==0) {
            // Scrape Standvirtual Ads
        } else {
            pid = wait(&status);
        }
    }
}