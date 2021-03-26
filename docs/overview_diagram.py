"""Create "overview" diagram for README file."""
# pylint: disable=pointless-statement

import diagrams
import diagrams.aws.compute as compute
import diagrams.aws.integration as integration
import diagrams.aws.network as network

diagram_attr = {
    'margin': '-0.8,-0.8',
    'size': '10,8',
    'bgcolor': 'transparent'
}
with diagrams.Diagram(
        '',
        show=False,
        filename='docs/overview',
        graph_attr=diagram_attr):

    msc_cluster_attr = {
        'margin': '8'
    }
    with diagrams.Cluster(
            'Minecraft Server Controller Project',
            graph_attr=msc_cluster_attr):

        hourly_event = integration.Eventbridge('Hourly Schedule')
        nightly_event = integration.Eventbridge('Nightly Schedule')

        sam_diagram_attr = {
            'margin': '20'
        }
        with diagrams.Cluster(
                'Serverless Application Model',
                graph_attr=sam_diagram_attr):
            api_gw = network.APIGateway('REST API')

            sf_idle = integration.StepFunctions(
                'State Machine -\nShutdown Idle Servers'
            )
            sf_stopall = integration.StepFunctions(
                'State Machine -\nStop All Servers'
            )
            hourly_event >> sf_idle
            nightly_event >> sf_stopall

            sam = compute.Lambda('')
            api_gw >> sam
            sf_idle >> sam
            sf_stopall >> sam

            func1 = compute.LambdaFunction('GET\n/servers/*/users')
            func2 = compute.LambdaFunction('GET | POST\n/servers/*')
            func3 = compute.LambdaFunction('GET\n/servers')
            funcs = [func1, func2, func3]

            sam - funcs

    msf_cluster_attr = {
        'margin': '60'
    }
    with diagrams.Cluster(
            'Minecraft Server Farm Project',
            graph_attr=msf_cluster_attr):
        game_servers = compute.EC2Instances('EC2 Game Servers')
        funcs >> game_servers
