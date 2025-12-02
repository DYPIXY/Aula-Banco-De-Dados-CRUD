use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
pub use user;

#[post("/user/create")]
async fn createUser(req_body: String) -> impl Responder 
{
    user::createUser(req_body);
}

#[post("/user/update")]
async fn updateUserByPk() -> impl Responder 
{
    user::updateUserByPk();
    HttpResponse::Ok().body("user");
}

#[get("/user/retrieve")]
async fn retrieveUserByPk() -> impl Responder 
{
    user::retrieveUserByPk();
}

#[post("/notes/create")]
async fn createNote() -> impl Responder 
{
    HttpResponse::Ok().body("user")
}

#[post("/notes/read")]
async fn readNote() -> impl Responder 
{
    HttpResponse::Ok().body("user")
}

#[post("/notes/update")]
async fn updateNote() -> impl Responder 
{
    HttpResponse::Ok().body("user")
}

#[post("/notes/delete")]
async fn deleteNote() -> impl Responder 
{
    HttpResponse::Ok().body("user")
}

//main 
#[actix_web::main]
async fn main() -> std::io::Result<()> 
{
    HttpServer::new(|| 
    {
        App::new()
            .service(createUser)
            .service(updateUserByPk)
            .service(retrieveUserByPk)
            .service(createNote)
            .service(readNote)
            .service(updateNote)
            .service(deleteNote)
            //.route("/hey", web::get().to(manual_hello))
    })
    .bind(("127.0.0.1", 6065))?
    .run()
    .await
}




