from dcim.models import Device
from extras.scripts import Script
from utilities.choices import DeviceStatusChoices # Importa as opções de status

class RelatorioContagemDispositivos(Script):
    """
    Este script conta o número total de dispositivos no NetBox
    e agrupa a contagem por cada status (ativo, planejado, etc.).
    """

    class Meta:
        name = "Contagem de Dispositivos por Status"
        description = "Mostra quantos dispositivos existem para cada status"

    def run(self, data, commit):
        """
        Lógica principal do relatório.
        """
        self.log_info("Iniciando a contagem de dispositivos por status...")

        # Pega todos os status possíveis para dispositivos
        status_choices = DeviceStatusChoices.choices

        total_geral = 0

        # Itera sobre cada status possível
        for status_slug, status_name in status_choices:
            # Para cada status, faz uma contagem no banco de dados
            # O método .count() é muito mais eficiente do que carregar todos os objetos
            count = Device.objects.filter(status=status_slug).count()

            if count > 0:
                # Loga o resultado para cada status que tem dispositivos
                self.log_success(None, f"Status '{status_name}': {count} dispositivos.")
                total_geral += count
            else:
                 self.log_info(f"Status '{status_name}': 0 dispositivos.")


        # Loga um resultado final com o total
        self.log_info(f"Contagem finalizada. Total de {total_geral} dispositivos registrados.")

        return "Relatório de contagem concluído."
