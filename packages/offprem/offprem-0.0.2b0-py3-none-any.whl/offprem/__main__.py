from offprem import ConfigureVPC


def main():
    """ Display the contents of the configuration file. """
    if ConfigureVPC.configuration_file.exists():
        ConfigureVPC().configuration_file_parser.sections()


if __name__ == '__main__':
    main()
