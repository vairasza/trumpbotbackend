import { Stack, Duration } from "aws-cdk-lib";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import {
  Cors,
  EndpointType,
  JsonSchemaType,
  LambdaIntegration,
  LambdaRestApi,
  Period,
} from "aws-cdk-lib/aws-apigateway";
import { resolve } from "path";

export class TrumpbotbackendStack extends Stack {
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

    const endpoint = api.root.addMethod("POST", new LambdaIntegration(lambda), {
      apiKeyRequired: true,
      requestModels: {
        //i think that we need an array here
        contentType: "application/json",
        modelName: "asd",
        schema: {
          type: JsonSchemaType.OBJECT,
          properties: {
            user_input: {
              type: JsonSchemaType.STRING,
            },
            fake_tweet: {
              type: JsonSchemaType.STRING,
            },
          },
          required: ["user_input", "fake_tweet"],
        },
      },
      methodResponses: [
        {
          statusCode: "200",
          responseModels: {
            user_input: {
              type: JsonSchemaType.STRING,
            },
            last_tweet: {
              type: JsonSchemaType.STRING,
            },
            fake_tweet: {
              type: JsonSchemaType.STRING,
            },
          },
        },
        {
          statusCode: "500",
          responseModels: {},
        },
      ],
    });

    const apiKey = api.addApiKey("TrumpbotApiKey", {
      apiKeyName: "trump-bot-api-key",
      value: process.env.TRUMPBOTAPIKEY,
    });

    const plan = api.addUsagePlan("TrumpbotUsagePlan", {
      throttle: {
        burstLimit: 5,
        rateLimit: 10,
      },
      quota: {
        limit: 100,
        period: Period.DAY,
      },
    });

    plan.addApiKey(apiKey);

    /*
    endPoint.addModel("SendData", {
      contentType: "application/json",
      modelName: "SendData",
      schema: {
        type: JsonSchemaType.OBJECT,
        properties: {
          user_input: {
            type: JsonSchemaType.STRING,
          },
          last_tweet: {
            type: JsonSchemaType.STRING,
          },
          fake_tweet: {
            type: JsonSchemaType.STRING,
          },
        },
      },
    });

    endPoint.addModel("ReceiveData", {
      contentType: "application/json",
      modelName: "ReceiveData",
      schema: {
        type: JsonSchemaType.OBJECT,
        properties: {
          statusCode: {
            type: JsonSchemaType.NUMBER,
          },
          body: {
            user_input: {
              type: JsonSchemaType.STRING,
            },
          },
        },
      },
    });

    endPoint.addMethodResponse({
      statusCode: "200",
      responseModels: {},
    });*/
  }
}
