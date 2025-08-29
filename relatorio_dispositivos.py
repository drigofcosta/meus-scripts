from dcim.models import Device
from extras.scripts import Script, ChoiceVar

class RelatorioDispositivoSemIPPrimario(Script):
    """
    Este script verifica quais dispositivos com um status específico
    não possuem um endereço IP primário (IPv4 ou IPv6) configurado.
    """

    class Meta:
        name = "Relatório de Dispositivos sem IP Primário"
        description = "Verifica dispositivos sem um endereço IP primário definido"

    STATUS_CHOICES = (
        ('active', 'Ativo'),
        ('planned', 'Planejado'),
        ('staging', 'Em Staging'),
    )

    status = ChoiceVar(
        choices=STATUS_CHOICES,
        label="Status do Dispositivo",
        description="Selecione o status dos dispositivos a serem verificados"
    )

    def run(self, data, commit):
        """
        Lógica principal do relatório.
        """
        status_selecionado = data['status']

        # Filtra os dispositivos com base no status selecionado
        dispositivos = Device.objects.filter(status=status_selecionado)

        if not dispositivos.exists():
            self.log_info(f"Nenhum dispositivo encontrado com o status '{status_selecionado}'.")
            return

        # Itera sobre cada dispositivo para verificar o IP primário
        for dispositivo in dispositivos:
            if not dispositivo.primary_ip:
                # Se não tiver IP primário, registra uma FALHA
                self.log_failure(
                    dispositivo,
                    f"O dispositivo não possui um endereço IP primário configurado."
                )
            else:
                # Se tiver IP primário, registra um SUCESSO
                self.log_success(
                    dispositivo,
                    f"O dispositivo possui um IP primário: {dispositivo.primary_ip}."
                )
