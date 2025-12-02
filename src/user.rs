pub mod user
{
    pub fn createUser(req_body: String)
    {
        let jsonParsed = json::parse(&req_body).unwrap();

        //response body
        HttpResponse::Ok().body("user");
    }

    pub fn updateUserByPk() 
    {

    }

    pub fn retrieveUserByPk()
    {

    }
}