import { Stack, Duration } from "aws-cdk-lib";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import {
  EndpointType,
  LambdaIntegration,
  RestApi,
} from "aws-cdk-lib/aws-apigateway";
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

    const restApi = new RestApi(this, "TrumpbotGateway", {
      restApiName: "Trumpbot Gateway",
      description: "This service handles API Calls",
      handler: lambda,
      endpointConfiguration: EndpointType.REGIONAL,
    });

    restApi.root.addMethod("POST", new LambdaIntegration(lambda, {}));
  }
}
