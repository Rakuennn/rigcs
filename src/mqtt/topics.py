# MQTT Topic definitions – single source of truth for both client and handler


class Topics:
    CMD_ACCESS = "rigcs/cmd/access"
    CMD_MASTER = "rigcs/cmd/master"
    CMD_REGISTER = "rigcs/cmd/register"

    RESULT_ACCESS = "rigcs/result/access"
    RESULT_MASTER = "rigcs/result/master"
    RESULT_REGISTER = "rigcs/result/register"

    CMD_ALL = "rigcs/cmd/#"
