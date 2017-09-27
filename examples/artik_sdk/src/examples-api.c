#include <stddef.h>
#include <shell/tash.h>

extern int sdk_main(int argc, char *argv[]);
extern int cloud_main(int argc, char *argv[]);
extern int gpio_main(int argc, char *argv[]);
extern int pwm_main(int argc, char *argv[]);
extern int adc_main(int argc, char *argv[]);
extern int http_main(int argc, char *argv[]);
extern int wifi_main(int argc, char *argv[]);
extern int websocket_main(int argc, char *argv[]);
extern int see_main(int argc, char *argv[]);

static tash_cmdlist_t atk_cmds[] = {
    {"sdk", sdk_main, TASH_EXECMD_SYNC},
    {"gpio", gpio_main, TASH_EXECMD_SYNC},
    {"pwm", pwm_main, TASH_EXECMD_SYNC},
    {"adc", adc_main, TASH_EXECMD_SYNC},
    {"cloud", cloud_main, TASH_EXECMD_SYNC},
    {"http", http_main, TASH_EXECMD_SYNC},
    {"wifi", wifi_main, TASH_EXECMD_SYNC},
    {"websocket", websocket_main, TASH_EXECMD_SYNC},
    {"see", see_main, TASH_EXECMD_SYNC},
    {NULL, NULL, 0}
};

int main(int argc, char *argv[])
{
#ifdef CONFIG_TASH
    /* add tash command */
    tash_cmdlist_install(atk_cmds);
#endif

    return 0;
}

