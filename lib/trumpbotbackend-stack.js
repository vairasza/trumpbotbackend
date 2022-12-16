import { Stack, Duration } from "aws-cdk-lib";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { Cors, EndpointType, LambdaRestApi } from "aws-cdk-lib/aws-apigateway";
import { resolve } from "path";

export class TrumpbotbackendStack extends Stack {
  /**
   *
   * @param {Construct} scope
   * @param {string} id
   * @param {StackProps=} props
   */
  constructor(scope, id, props) {
    super(scope, id, props);

    const lambda = new Function(this, "TrumpbotLambda", {
      runtime: Runtime.PYTHON_3_8,
      memorySize: 512,
      timeout: Duration.seconds(10),
      handler: "handler.handler",
      code: Code.fromAsset(resolve("./src/lambda")),
    });

    const api = new LambdaRestApi(this, "TrumpbotGateway", {
      restApiName: "Trumpbot Gateway",
      description: "This service handles API Calls from Trumpbot Frontend",
      handler: lambda,
      endpointConfiguration: {
        types: [EndpointType.REGIONAL],
      },
      defaultCorsPreflightOptions: {
        allowOrigins: Cors.ALL_ORIGINS,
        allowMethods: ["POST", "OPTIONS"],
      },
      proxy: false,
    });

    const resource = api.root.addResource("v1");
    const endPoint = resource.addMethod("POST");

    api.addUsagePlan("TrumpbotUsagePlan", {
      name: "TrumpbotUsagePlan",
      throttle: {
        rateLimit: 15,
        burstLimit: 3,
      },
    });

    endPoint.addMethodResponse({
      statusCode: "200",
      responseModels: {
        type: "object",
        properties: {
          user_input: {
            type: "string",
          },
          last_tweet: {
            type: "string",
          },
          fake_tweet: {
            type: "string",
          },
        },
      },
    });
  }
}
