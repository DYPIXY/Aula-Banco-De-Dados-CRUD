use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder, Json};
mod user;
mod notes;

#[post("/user/create")]
async fn createUser(req_body: String) -> impl Responder 
{
    createUser(req_body);
    HttpResponse::Ok().body("User created");
}

#[post("/user/update")]
async fn updateUserByPk() -> impl Responder 
{
    updateUserByPk();
    HttpResponse::Ok().body("user");
}

#[get("/user/retrieve")]
async fn retrieveUserByPk() -> impl Responder 
{
    retrieveUserByPk();
    HttpResponse::Ok().body("user");
}

#[post("/notes/create")]
async fn createNote() -> impl Responder 
{
    createNote();
    HttpResponse::Ok().body("user");
}

#[post("/notes/read")]
async fn readNote() -> impl Responder 
{
    readNote();
    HttpResponse::Ok().body("user");
}

#[post("/notes/update")]
async fn updateNote() -> impl Responder 
{
    updateNote();
    HttpResponse::Ok().body("user");
}

#[post("/notes/delete")]
async fn deleteNote() -> impl Responder 
{
    deleteNote();
    HttpResponse::Ok().body("user");
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




